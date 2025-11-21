"""
Database Models for SentraOS
Defines SQLAlchemy models for storing system metrics, scan results, and alerts
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class SystemMetric(Base):
    """Store system performance metrics"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    metric_type = Column(String(50))  # cpu, memory, disk, network
    value = Column(Float)
    unit = Column(String(20))
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.now)


class ScanResult(Base):
    """Store security scan results"""
    __tablename__ = 'scan_results'
    
    id = Column(Integer, primary_key=True)
    target = Column(String(100))
    scan_type = Column(String(50))
    status = Column(String(20))
    open_ports = Column(JSON)
    vulnerabilities = Column(JSON)
    risk_level = Column(String(20))
    timestamp = Column(DateTime, default=datetime.now)


class Alert(Base):
    """Store security and performance alerts"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    alert_type = Column(String(50))
    severity = Column(String(20))
    message = Column(Text)
    details = Column(JSON)
    acknowledged = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.now)


class ActivityLog(Base):
    """Store system activity logs"""
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True)
    action = Column(String(100))
    description = Column(Text)
    user = Column(String(50), default='system')
    timestamp = Column(DateTime, default=datetime.now)


# Database setup
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'sentra.db')
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def get_session():
    """Get a new database session"""
    return Session()


def log_activity(action: str, description: str, user: str = 'system'):
    """Helper function to log activities"""
    session = get_session()
    log = ActivityLog(action=action, description=description, user=user)
    session.add(log)
    session.commit()
    session.close()
