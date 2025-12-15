from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, func
from app.extensions import db

patient_medicines = Table(
    'patient_medicines',
    db.metadata,
    Column('patient_id', Integer, ForeignKey('patients.id'), primary_key=True),
    Column('medicine_id', Integer, ForeignKey('medicines.id'), primary_key=True),
    Column('dose_per_take', String(50), default='1'),
    Column('notes', Text, default=''),
    Column('created_at', DateTime, default=func.current_timestamp())
)

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quit = db.Column(db.Boolean, default=False, nullable=False)
    
    @classmethod
    def from_patient(cls, patient, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = ['id', 'created_at']
        
        data = {}
        for column in cls.__table__.columns.keys():
            if column not in exclude_fields:
                data[column] = getattr(patient, column, None)
        
        return cls(**data)
    
    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
            "instructions": self.instructions,
            "quit": self.quit,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_sensitive:
            data['medicines'] = [
                {
                    'id': m.id,
                    'name': m.name,
                    'dosage': m.dosage,
                    'frequency_hours': m.frequency_hours,
                    'is_active': m.is_active
                } for m in self.medicines.all()
            ]
            data['medicine_count'] = self.medicines.count()
        
        return data
