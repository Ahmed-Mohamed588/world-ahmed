// SentraOS Dashboard JavaScript

// Chart.js instances
let systemChart = null;
let networkChart = null;

// Data storage
const cpuData = [];
const memoryData = [];
const networkSendData = [];
const networkRecvData = [];
const timeLabels = [];
const maxDataPoints = 20;

// Initialize charts
function initCharts() {
    const systemCtx = document.getElementById('systemChart').getContext('2d');
    systemChart = new Chart(systemCtx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [
                {
                    label: 'CPU %',
                    data: cpuData,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Memory %',
                    data: memoryData,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });

    const networkCtx = document.getElementById('networkChart').getContext('2d');
    networkChart = new Chart(networkCtx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [
                {
                    label: 'Send (MB/s)',
                    data: networkSendData,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Receive (MB/s)',
                    data: networkRecvData,
                    borderColor: 'rgb(153, 102, 255)',
                    backgroundColor: 'rgba(153, 102, 255, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}

// Update time display
function updateTime() {
    const now = new Date();
    document.getElementById('current-time').textContent = now.toLocaleString();
}

// Fetch and update metrics
async function updateMetrics() {
    try {
        const response = await fetch('/api/metrics/current');
        const metrics = await response.json();

        // Update stat cards
        document.getElementById('cpu-stat').textContent = `${metrics.cpu.usage_percent.toFixed(1)}%`;
        document.getElementById('memory-stat').textContent = `${metrics.memory.percent.toFixed(1)}%`;
        document.getElementById('disk-stat').textContent = `${metrics.disk.percent.toFixed(1)}%`;

        // Update chart data
        const timeLabel = new Date().toLocaleTimeString();
        
        if (timeLabels.length >= maxDataPoints) {
            timeLabels.shift();
            cpuData.shift();
            memoryData.shift();
            networkSendData.shift();
            networkRecvData.shift();
        }

        timeLabels.push(timeLabel);
        cpuData.push(metrics.cpu.usage_percent);
        memoryData.push(metrics.memory.percent);
        networkSendData.push(metrics.network.send_rate_mbps);
        networkRecvData.push(metrics.network.recv_rate_mbps);

        // Update charts
        systemChart.update();
        networkChart.update();

    } catch (error) {
        console.error('Error updating metrics:', error);
    }
}

// Fetch and display alerts
async function updateAlerts() {
    try {
        const response = await fetch('/api/alerts?limit=10');
        const alerts = await response.json();

        const container = document.getElementById('alerts-container');
        
        if (alerts.length === 0) {
            container.innerHTML = '<p class="text-muted">No alerts</p>';
        } else {
            container.innerHTML = alerts.map(alert => `
                <div class="alert-item severity-${alert.severity}">
                    <div class="d-flex justify-content-between">
                        <strong>${alert.type.toUpperCase()}</strong>
                        <span class="badge bg-${getSeverityColor(alert.severity)}">${alert.severity}</span>
                    </div>
                    <p class="mb-1">${alert.message}</p>
                    <div class="alert-time">${new Date(alert.timestamp).toLocaleString()}</div>
                </div>
            `).join('');
        }

        // Update alert count
        document.getElementById('alert-count').textContent = alerts.length;

    } catch (error) {
        console.error('Error updating alerts:', error);
    }
}

// Fetch and display scan results
async function updateScans() {
    try {
        const response = await fetch('/api/security/scans?limit=5');
        const scans = await response.json();

        const container = document.getElementById('scan-results');
        
        if (scans.length === 0) {
            container.innerHTML = '<p class="text-muted">No recent scans</p>';
        } else {
            container.innerHTML = scans.map(scan => `
                <div class="scan-result risk-${scan.risk_level}">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong>${scan.target}</strong>
                            <span class="badge bg-${getRiskColor(scan.risk_level)} ms-2">${scan.risk_level} risk</span>
                        </div>
                        <small class="text-muted">${new Date(scan.timestamp).toLocaleString()}</small>
                    </div>
                    <div class="mt-2">
                        <small>Open Ports: ${scan.open_ports.length}</small> |
                        <small>Vulnerabilities: ${scan.vulnerabilities.length}</small>
                    </div>
                    ${scan.vulnerabilities.length > 0 ? `
                        <div class="mt-2">
                            ${scan.vulnerabilities.slice(0, 3).map(v => `
                                <div class="vulnerability-item">
                                    <i class="fas fa-exclamation-triangle"></i> ${v.name} - ${v.description}
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

    } catch (error) {
        console.error('Error updating scans:', error);
    }
}

// Fetch and display network connections
async function updateConnections() {
    try {
        const response = await fetch('/api/network/connections');
        const connections = await response.json();

        const tbody = document.getElementById('connections-body');
        
        if (connections.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-muted">No active connections</td></tr>';
        } else {
            tbody.innerHTML = connections.map(conn => `
                <tr>
                    <td><code>${conn.local_address}</code></td>
                    <td><code>${conn.remote_address}</code></td>
                    <td><span class="badge bg-success">${conn.status}</span></td>
                    <td>${conn.pid || 'N/A'}</td>
                </tr>
            `).join('');
        }

    } catch (error) {
        console.error('Error updating connections:', error);
    }
}

// Run security scan
async function runSecurityScan() {
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Scanning...';
    button.disabled = true;

    try {
        const response = await fetch('/api/security/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                target: 'localhost',
                type: 'quick'
            })
        });

        const result = await response.json();
        
        if (result.error) {
            alert('Scan error: ' + result.error);
        } else {
            // Refresh scan results
            await updateScans();
        }

    } catch (error) {
        console.error('Error running scan:', error);
        alert('Failed to run security scan');
    } finally {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// Helper functions
function getSeverityColor(severity) {
    const colors = {
        low: 'info',
        medium: 'warning',
        high: 'danger',
        critical: 'dark'
    };
    return colors[severity] || 'secondary';
}

function getRiskColor(risk) {
    const colors = {
        low: 'success',
        medium: 'warning',
        high: 'danger'
    };
    return colors[risk] || 'secondary';
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    updateTime();
    updateMetrics();
    updateAlerts();
    updateScans();
    updateConnections();

    // Update time every second
    setInterval(updateTime, 1000);

    // Update metrics every 3 seconds
    setInterval(updateMetrics, 3000);

    // Update alerts every 5 seconds
    setInterval(updateAlerts, 5000);

    // Update scans every 10 seconds
    setInterval(updateScans, 10000);

    // Update connections every 5 seconds
    setInterval(updateConnections, 5000);
});
