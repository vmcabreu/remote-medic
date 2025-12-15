from app.models.patients import Patient, db
from app.models.user import User, db
from app.utils.mappers.generic_mapper import GenericMapper
from typing import Any, Dict, List, Optional, Type, Union


def get_all_patients():
    """
    Obtiene todos los pacientes del sistema
    """
    return Patient.query.all()

def get_patient_by_id(patient_id: int):
    """
    Obtiene un paciente específico por su ID
    """
    return Patient.query.get(patient_id)

def patient_exists(patient_id: int):
    """
    Verifica si existe un paciente con el ID dado
    """
    return Patient.query.get(patient_id) is not None


def get_patients_paginated(page: int = 1, per_page: int = 10):
    """
    Obtiene pacientes paginados con metadatos de paginación
    """
    return Patient.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )


def get_patients_by_carer_id(carer_id: int):
    """
    Obtiene TODOS los pacientes asignados a un cuidador específico (user_id)
    usando la relación many-to-many
    """
    user = User.query.get(carer_id)
    if not user:
        return []
    return user.patients.all()

def get_user_patients(user_id: int):
    """
    Obtiene pacientes asignados a un usuario (alias de get_patients_by_carer_id)
    """
    return get_patients_by_carer_id(user_id)


def assign_patient_to_user(user_id: int, patient_id: int):
    """
    Asigna un paciente a un usuario/cuidador
    """
    user = User.query.get(user_id)
    patient = Patient.query.get(patient_id)
    
    if user and patient:
    
        if patient not in user.patients.all():
            user.patients.append(patient)
            db.session.commit()
            return True
    return False

def remove_patient_from_user(user_id: int, patient_id: int):
    """
    Remueve la asignación de un paciente de un usuario/cuidador
    """
    user = User.query.get(user_id)
    patient = Patient.query.get(patient_id)
    
    if user and patient and patient in user.patients.all():
        user.patients.remove(patient)
        db.session.commit()
        return True
    return False

def get_patient_users(patient_id: int):
    """
    Obtiene todos los usuarios/cuidadores asignados a un paciente
    """
    patient = Patient.query.get(patient_id)
    return patient.assigned_users.all() if patient else []


def create_patient(patient: Patient):
    """
    Crea un nuevo paciente en la base de datos
    """
    new_patient = Patient.from_patient(patient)
    db.session.add(new_patient)
    db.session.commit()
    return new_patient

def update_patient(patient_id: int, patient_data: Union[Dict, Any]) -> Optional[Any]:
    """
    Actualiza un paciente existente con los datos proporcionados
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return None
    
    GenericMapper.update_model(patient, patient_data)
    db.session.commit()
    return patient

def delete_patient(patient_id: int):
    """
    Elimina un paciente y todas sus asignaciones relacionadas (CASCADE)
    """
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return True
    return False
