from datetime import datetime, timedelta
import os

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import jwt

class User(db.Model):
    __tablename__ = "users"
    
    user_patient_assignment = db.Table('user_patient_assignments',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow),
    db.Column('role', db.String(50), default='assigned')
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    work_start_time = db.Column(db.Time, nullable=True)  
    work_end_time = db.Column(db.Time, nullable=True) 
    work_days = db.Column(db.String(50), default='mon,tue,wed,thu,fri')
    is_available = db.Column(db.Boolean, default=True)     
    patients = db.relationship('Patient', 
                             secondary=user_patient_assignment,
                             backref=db.backref('assigned_users', lazy='dynamic'),
                             lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Obtener nombre completo"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def generate_token(self):        
        identity_str = str(self.id)  
        additional_claims = {
            'username': self.username,
            'is_admin': self.is_admin
        }
        return create_access_token(identity=identity_str, additional_claims=additional_claims)
    @staticmethod
    def verify_token(token):
        """Verificar JWT token"""
        try:
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY', 'dev-secret-key'),
                algorithms=['HS256']
            )
            user_id = payload.get('sub')
            return User.query.get(user_id)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def update_last_login(self):
        """Actualizar último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()
        
        
    def is_in_working_hours(self):
        """Verifica si el usuario está en horario laboral actual"""
        now = datetime.utcnow()
        current_time = now.time()
        current_day = now.strftime('%a').lower()
                
        work_days_list = self.work_days.split(',')
        if current_day not in [day.strip() for day in work_days_list]:
            return False
                    
        if self.work_start_time and self.work_end_time:
            return self.work_start_time <= current_time <= self.work_end_time
            
        return self.is_available

    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'work_start_time': self.work_start_time.isoformat() if self.work_start_time else None,
            'work_end_time': self.work_end_time.isoformat() if self.work_end_time else None,
            'work_days': self.work_days,
            'is_available': self.is_available,
            'in_working_hours': self.is_in_working_hours()
        }
        
        if include_sensitive:
            data['patient_count'] = self.patients.count()
            data['patients'] = [
                {
                    'id': p.id,
                    'first_name': p.name,
                    'last_name': p.surname,
                    'full_name': f"{p.name or ''} {p.surname or ''}".strip() or str(p.id)
                }
                for p in self.patients.all()
            ]
        
        return data


    def __repr__(self):
        return f'<User {self.username}>'
