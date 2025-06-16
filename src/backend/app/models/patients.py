from datetime import datetime
from app.extensions import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quit = db.Column(db.Boolean, default=False,nullable=False)


    @classmethod
    def from_patient(cls, patient, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = ['id', 'created_at', 'updated_at']
        
        data = {}
        for column in cls.__table__.columns.keys():
            if column not in exclude_fields:
                data[column] = getattr(patient, column, None)
        
        return cls(**data)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
            "instructions": self.instructions,
            "created_at": self.created_at.isoformat(),
        }
