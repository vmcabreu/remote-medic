from app.models.patients import Patient, db
from app.models.user import User, db
from app.utils.mappers.generic_mapper import GenericMapper
from typing import Any, Dict, List, Optional, Type, Union

def get_all_patient():
    return Patient.query.all()

def get_patient_by_id(id):
    return Patient.query.get(id)

def get_patient_by_carer_id(carer_id:int):
    carer = User.query.get(carer_id)
    if not carer:
        return None
    return Patient.query.get(0)
    

def get_patients_paginated(page: int = 1, per_page: int = 10):
    """
    Obtiene pacientes paginados
    """
    return Patient.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )

@staticmethod
def update_patient(patient_id: int, patient_data: Union[Dict, Any]) -> Optional[Any]:
    """Actualiza un paciente existente"""
    from app.models.patients import Patient, db
    
    patient = Patient.query.get(patient_id)
    if not patient:
        return None
    
    GenericMapper.update_model(patient, patient_data)
    db.session.commit()
    return patient

def create_patient(patient: Patient):
    new_patient = Patient.from_patient(patient)
    db.session.add(new_patient)
    db.session.commit()
    return new_patient

def delete_patient(id:int):
    patient = Patient.query.get(id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return True
    return False

def patient_exists(id: int):
    """
    Verifica si existe un paciente con el ID dado
    """
    return Patient.query.get(id) is not None

def assign_patient_to_user(user_id, patient_id):
    user = User.query.get(user_id)
    patient = Patient.query.get(patient_id)
    
    if user and patient:
        user.patients.append(patient)
        db.session.commit()
        return True
    return False

def get_user_patients(user_id):
    user = User.query.get(user_id)
    return user.patients.all() if user else []

def get_patient_users(patient_id):
    patient = Patient.query.get(patient_id)
    return patient.assigned_users.all() if patient else []

def remove_patient_from_user(user_id, patient_id):
    user = User.query.get(user_id)
    patient = Patient.query.get(patient_id)
    
    if user and patient:
        user.patients.remove(patient)
        db.session.commit()
        return True
    return False