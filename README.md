# SentraOS: Smart Operations & Security Platform

A comprehensive Python-based security monitoring and operations platform that provides real-time network monitoring, security scanning, automated alerts, and a beautiful web dashboard.

## 🚀 Features

- **Real-time System Monitoring**: Track CPU, RAM, disk usage, and network metrics
- **Security Scanning**: Automated port scanning and vulnerability detection using nmap
- **Alert System**: Intelligent alerts for security threats and performance issues
- **Automation**: Scheduled monitoring and security scans with APScheduler
- **Web Dashboard**: Professional Flask-based dashboard with Chart.js visualizations
- **Database**: SQLite database for storing metrics, scan results, and alerts

## 📁 Project Structure

```
SentraOS/
├── network_monitor/          # System metrics monitoring module
│   └── monitor.py           # psutil-based system monitoring
├── security_scanner/         # Security scanning module
│   └── scanner.py           # nmap-based vulnerability scanner
├── automation/               # Automation & scheduling module
│   └── auto_responder.py    # APScheduler-based task automation
├── dashboard/                # Flask web application
│   ├── app.py               # Main Flask application
│   ├── templates/           # HTML templates
│   │   └── index.html
│   └── static/              # CSS and JavaScript
│       ├── css/style.css
│       └── js/dashboard.js
├── models.py                 # SQLAlchemy database models
├── sentra.db                 # SQLite database (auto-created)
└── README.md
```

## 🛠️ Technologies Used

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Monitoring**: psutil (system metrics)
- **Security**: python-nmap (network scanning)
- **Automation**: APScheduler (task scheduling)
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Chart.js, Vanilla JavaScript

## 🏃 Quick Start

The application is configured to run automatically. Simply click the **Run** button and the dashboard will be available.

### Default Configuration:
- **Web Interface**: Accessible at the provided Replit URL
- **Port**: 5000
- **Auto Scans**: 
  - System metrics checked every 30 seconds
  - Security scans run every 5 minutes

## 📊 Dashboard Features

### Real-time Metrics
- CPU usage monitoring
- Memory (RAM) utilization
- Disk space tracking
- Network traffic analysis

### Security Scanning
- Quick vulnerability scans
- Port scanning (common ports)
- Risk level assessment
- Vulnerability detection

### Alert System
- Performance alerts (high CPU, memory, disk usage)
- Security alerts (vulnerabilities detected)
- Multiple severity levels (low, medium, high, critical)
- Alert acknowledgment system

### Visualizations
- Real-time CPU & Memory charts
- Network traffic graphs
- Active network connections table
- Recent scan results
- Alert timeline

## 🔒 Security Features

- **Port Scanning**: Detect open ports and services
- **Vulnerability Detection**: Identify common security risks
- **Risk Assessment**: Automatic risk level calculation
- **Network Monitoring**: Track active connections
- **Automated Alerts**: Real-time security notifications

## 🗄️ Database Schema

### Tables:
- `system_metrics`: Stores CPU, memory, disk, network metrics
- `scan_results`: Security scan results and vulnerabilities
- `alerts`: Security and performance alerts
- `activity_logs`: System activity logging

## 🔧 API Endpoints

- `GET /api/metrics/current` - Get current system metrics
- `GET /api/metrics/history` - Historical metrics data
- `POST /api/security/scan` - Run security scan
- `GET /api/security/scans` - Get scan history
- `GET /api/alerts` - Get recent alerts
- `POST /api/alerts/<id>/acknowledge` - Acknowledge alert
- `GET /api/network/connections` - Active connections
- `GET /api/tasks` - Scheduled tasks status
- `GET /api/stats` - Dashboard statistics

## 📈 Automated Tasks

The system runs the following automated tasks:

1. **System Health Check** (every 30 seconds)
   - Monitor CPU, memory, disk usage
   - Create alerts for threshold violations
   - Store metrics in database

2. **Security Scan** (every 5 minutes)
   - Scan localhost for vulnerabilities
   - Detect open ports and services
   - Generate security alerts

## 🎯 Use Cases

- **DevOps Monitoring**: Track system performance in real-time
- **Security Auditing**: Regular vulnerability assessments
- **Network Analysis**: Monitor network traffic and connections
- **Alert Management**: Proactive issue detection
- **Academic Projects**: Learn about security, monitoring, and automation

## 🚀 Future Enhancements

- Multi-host monitoring support
- Email/webhook notifications
- Advanced network traffic analysis
- Custom security rules engine
- Historical trend analysis
- Export reports (PDF, CSV)
- Integration with external security tools

## 📝 Notes

- **Root Access**: Some security scans may require elevated permissions
- **Performance**: Monitoring runs in background without impacting performance
- **Scalability**: Modular design allows easy addition of new features
- **Security**: Database and sessions are secured with environment variables

## 🧪 Development

### Module Architecture:
Each module is independently developed and can be extended:

- **Network Monitor**: Add new system metrics or external host monitoring
- **Security Scanner**: Add custom vulnerability checks or scan types
- **Automation**: Add new scheduled tasks or response actions
- **Dashboard**: Add new visualizations or API endpoints

### Database:
SQLAlchemy ORM makes it easy to extend the database schema and add new tables or fields.

## 📜 License

This project is designed for educational and monitoring purposes. Use responsibly and only scan networks you have permission to assess.

---

**SentraOS** - Smart Operations & Security Platform
Built with Python, Flask, and modern web technologies.
