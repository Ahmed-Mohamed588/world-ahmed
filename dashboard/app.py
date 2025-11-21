"""
SentraOS Dashboard
Main Flask application for the web-based monitoring and security platform
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from network_monitor.monitor import SystemMonitor
from security_scanner.scanner import SecurityScanner
from automation.auto_responder import AutoResponder
from models import get_session, SystemMetric, ScanResult, Alert, log_activity

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'sentra-dev-secret-key')

# Initialize modules
system_monitor = SystemMonitor()
security_scanner = SecurityScanner()
auto_responder = AutoResponder()


# Automated monitoring tasks
def periodic_system_check():
    """Periodic system metrics check"""
    session = None
    try:
        metrics = system_monitor.get_all_metrics()
        
        # Check for performance issues
        if metrics['cpu']['usage_percent'] > 80:
            auto_responder.create_alert(
                'performance',
                'high',
                f"High CPU usage detected: {metrics['cpu']['usage_percent']}%",
                {'cpu_data': metrics['cpu']}
            )
        
        if metrics['memory']['percent'] > 85:
            auto_responder.create_alert(
                'performance',
                'high',
                f"High memory usage detected: {metrics['memory']['percent']}%",
                {'memory_data': metrics['memory']}
            )
        
        if metrics['disk']['percent'] > 90:
            auto_responder.create_alert(
                'performance',
                'critical',
                f"Critical disk usage: {metrics['disk']['percent']}%",
                {'disk_data': metrics['disk']}
            )
        
        # Store metrics in database with proper session management
        session = get_session()
        session.add(SystemMetric(
            metric_type='cpu',
            value=metrics['cpu']['usage_percent'],
            unit='percent',
            details=metrics['cpu']
        ))
        session.add(SystemMetric(
            metric_type='memory',
            value=metrics['memory']['percent'],
            unit='percent',
            details=metrics['memory']
        ))
        session.commit()
        
    except Exception as e:
        print(f"Error in periodic system check: {e}")
    finally:
        if session:
            session.close()


def periodic_security_scan():
    """Periodic security scan"""
    session = None
    try:
        scan_result = security_scanner.quick_vulnerability_scan('localhost')
        
        # Store scan result with proper session management
        session = get_session()
        session.add(ScanResult(
            target=scan_result['target'],
            scan_type='vulnerability',
            status=scan_result['status'],
            open_ports=scan_result.get('open_ports', []),
            vulnerabilities=scan_result.get('vulnerabilities', []),
            risk_level=scan_result.get('risk_level', 'low')
        ))
        session.commit()
        
        # Create alerts for vulnerabilities
        if scan_result.get('vulnerabilities'):
            for vuln in scan_result['vulnerabilities']:
                auto_responder.create_alert(
                    'security',
                    vuln['severity'],
                    f"Vulnerability detected: {vuln['name']}",
                    {'vulnerability': vuln, 'target': scan_result['target']}
                )
        
    except Exception as e:
        print(f"Error in periodic security scan: {e}")
    finally:
        if session:
            session.close()


# Start automation tasks
auto_responder.add_periodic_task(periodic_system_check, 30, 'system_check')
auto_responder.add_periodic_task(periodic_security_scan, 300, 'security_scan')
auto_responder.start()


# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/metrics/current')
def get_current_metrics():
    """Get current system metrics"""
    try:
        metrics = system_monitor.get_all_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/history')
def get_metrics_history():
    """Get historical metrics data"""
    session = None
    try:
        metric_type = request.args.get('type', 'cpu')
        limit = int(request.args.get('limit', 20))
        
        session = get_session()
        metrics = session.query(SystemMetric)\
            .filter_by(metric_type=metric_type)\
            .order_by(SystemMetric.timestamp.desc())\
            .limit(limit)\
            .all()
        
        data = [{
            'timestamp': m.timestamp.isoformat(),
            'value': m.value,
            'unit': m.unit,
            'details': m.details
        } for m in reversed(metrics)]
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if session:
            session.close()


def is_valid_scan_target(target: str) -> bool:
    """Validate scan target to prevent SSRF attacks"""
    allowed_targets = ['localhost', '127.0.0.1', '::1']
    
    # Allow only localhost and local loopback addresses
    if target in allowed_targets:
        return True
    
    # Optionally allow local network ranges (commented out for security)
    # import ipaddress
    # try:
    #     ip = ipaddress.ip_address(target)
    #     return ip.is_private or ip.is_loopback
    # except ValueError:
    #     pass
    
    return False


@app.route('/api/security/scan', methods=['POST'])
def run_security_scan():
    """Trigger a security scan"""
    session = None
    try:
        data = request.json or {}
        target = data.get('target', 'localhost')
        scan_type = data.get('type', 'quick')
        
        # Security: Validate target to prevent SSRF
        if not is_valid_scan_target(target):
            return jsonify({
                'error': 'Invalid target. Only localhost scanning is permitted.',
                'allowed_targets': ['localhost', '127.0.0.1']
            }), 403
        
        if scan_type == 'quick':
            result = security_scanner.quick_vulnerability_scan(target)
        else:
            port_range = data.get('port_range', '1-1000')
            result = security_scanner.scan_host(target, port_range)
        
        # Store scan result with proper session management
        session = get_session()
        session.add(ScanResult(
            target=result['target'],
            scan_type=scan_type,
            status=result['status'],
            open_ports=result.get('open_ports', []),
            vulnerabilities=result.get('vulnerabilities', []),
            risk_level=result.get('risk_level', 'low')
        ))
        session.commit()
        
        log_activity('security_scan', f'Security scan performed on {target}')
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if session:
            session.close()


@app.route('/api/security/scans')
def get_scan_history():
    """Get scan history"""
    session = None
    try:
        limit = int(request.args.get('limit', 10))
        
        session = get_session()
        scans = session.query(ScanResult)\
            .order_by(ScanResult.timestamp.desc())\
            .limit(limit)\
            .all()
        
        data = [{
            'id': s.id,
            'target': s.target,
            'scan_type': s.scan_type,
            'status': s.status,
            'open_ports': s.open_ports,
            'vulnerabilities': s.vulnerabilities,
            'risk_level': s.risk_level,
            'timestamp': s.timestamp.isoformat()
        } for s in scans]
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if session:
            session.close()


@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    try:
        limit = int(request.args.get('limit', 20))
        severity = request.args.get('severity')
        
        alerts = auto_responder.get_alerts(limit, severity)
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/alerts/<int:alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    try:
        success = auto_responder.acknowledge_alert(alert_id)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/network/connections')
def get_network_connections():
    """Get active network connections"""
    try:
        connections = system_monitor.get_network_connections()
        return jsonify(connections)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks')
def get_tasks():
    """Get scheduled tasks status"""
    try:
        tasks = auto_responder.get_task_status()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_dashboard_stats():
    """Get overall dashboard statistics"""
    session = None
    try:
        session = get_session()
        
        total_scans = session.query(ScanResult).count()
        critical_alerts = session.query(Alert).filter_by(severity='critical').count()
        
        recent_scans = session.query(ScanResult)\
            .order_by(ScanResult.timestamp.desc())\
            .limit(5)\
            .all()
        
        high_risk_scans = sum(1 for s in recent_scans if s.risk_level == 'high')
        
        metrics = system_monitor.get_all_metrics()
        
        stats = {
            'total_scans': total_scans,
            'critical_alerts': critical_alerts,
            'high_risk_scans': high_risk_scans,
            'current_cpu': metrics['cpu']['usage_percent'],
            'current_memory': metrics['memory']['percent'],
            'current_disk': metrics['disk']['percent'],
            'system_status': 'healthy' if metrics['cpu']['usage_percent'] < 80 else 'warning'
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if session:
            session.close()


if __name__ == '__main__':
    log_activity('system_start', 'SentraOS Dashboard started')
    app.run(host='0.0.0.0', port=5000, debug=True)
