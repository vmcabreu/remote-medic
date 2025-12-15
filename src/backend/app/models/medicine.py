from app.extensions import db
from datetime import datetime

class Medicine(db.Model):
    __tablename__ = "medicines"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    dosage = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    
    frequency_hours = db.Column(db.Integer, nullable=True)
    frequency_days = db.Column(db.Integer, nullable=True)
    
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'name': self.name,
            'dosage': self.dosage,
            'description': self.description,
            'instructions': self.instructions,
            'frequency_hours': self.frequency_hours,
            'frequency_days': self.frequency_days,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensitive:
            data['patient_count'] = getattr(self, 'assigned_patients', []).count() if hasattr(self, 'assigned_patients') else 0
            
        return data
    
    def __repr__(self):
        return f'<Medicine {self.name}>'
