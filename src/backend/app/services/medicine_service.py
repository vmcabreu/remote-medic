from app.models.patients import Patient, db
from app.models.medicine import Medicine, db
from app.utils.mappers.generic_mapper import GenericMapper
from sqlalchemy import or_, func


def get_all_medicines(active_only):
    """Obtener todas las medicinas (opcional solo activas)"""
    query = Medicine.query
    if active_only:
        query = query.filter_by(is_active=active_only)
    return query.all()

def get_medicine_by_id(medicine_id):
    """Obtener medicina por ID"""
    return Medicine.query.get(medicine_id)

def get_medicines_paginated(page: int = 1, per_page: int = 10):
    """Obtener medicinas paginadas"""
    return Medicine.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )

def create_medicine(medicine_data):
    """Crear nueva medicina"""
    medicine = Medicine(**medicine_data)
    db.session.add(medicine)
    db.session.commit()
    return medicine

def update_medicine(medicine_id, medicine_data):
    """Actualizar medicina existente"""
    medicine = get_medicine_by_id(medicine_id)
    if not medicine:
        return None
    
    GenericMapper.update_model(medicine, medicine_data)
    medicine.updated_at = func.now()
    db.session.commit()
    return medicine

def delete_medicine(medicine_id):
    """Eliminar medicina"""
    medicine = get_medicine_by_id(medicine_id)
    if medicine:
        db.session.delete(medicine)
        db.session.commit()
        return True
    return False


def assign_medicine_to_patient(patient_id, medicine_id, dose_per_take='1', notes=None):
    """Asignar medicina a paciente"""
    patient = Patient.query.get(patient_id)
    medicine = Medicine.query.get(medicine_id)
    
    if not patient or not medicine:
        return False
    

    if medicine in patient.medicines.all():
        return False 
    
    patient.medicines.append(medicine)
    db.session.commit()
    return True

def get_patient_medicines(patient_id):
    """Obtener todas las medicinas de un paciente"""
    patient = Patient.query.get(patient_id)
    return patient.medicines.all() if patient else []

def remove_medicine_from_patient(patient_id, medicine_id):
    """Quitar medicina de paciente"""
    patient = Patient.query.get(patient_id)
    medicine = Medicine.query.get(medicine_id)
    
    if not patient or not medicine:
        return False
    
    if medicine in patient.medicines.all():
        patient.medicines.remove(medicine)
        db.session.commit()
        return True
    
    return False


def search_medicines(query, active_only=True):
    """Buscar medicinas por nombre"""
    base_query = Medicine.query.filter(Medicine.name.ilike(f'%{query}%'))
    
    if active_only:
        base_query = base_query.filter_by(is_active=True)
    
    return base_query.limit(20).all()

def get_medicines_by_frequency(frequency_hours=None, frequency_days=None):
    """Obtener medicinas por frecuencia"""
    query = Medicine.query
    
    if frequency_hours:
        query = query.filter_by(frequency_hours=frequency_hours)
    
    if frequency_days:
        query = query.filter_by(frequency_days=frequency_days)
    
    return query.all()


def get_medicine_stats():
    """Estadísticas generales de medicinas"""
    total = db.session.query(func.count()).select_from(Medicine).scalar()
    active = db.session.query(func.count()).select_from(Medicine).filter_by(is_active=True).scalar()
    
    return {
        'total_medicines': total,
        'active_medicines': active,
        'inactive_medicines': total - active
    }
