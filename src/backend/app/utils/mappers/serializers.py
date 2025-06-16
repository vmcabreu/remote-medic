def serialize_patient(patient):
    return {
        'id': patient.id,
        'name': patient.name,
        'email': patient.email,
        'phone': patient.phone,
        'created_at': patient.created_at.isoformat() if patient.created_at else None
    }

def serialize_patients(patients):
    return [serialize_patient(patient) for patient in patients]