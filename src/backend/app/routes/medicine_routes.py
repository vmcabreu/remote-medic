from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.patients import Patient, patient_medicines
from app.models.medicine import Medicine, db
from app.services.medicine_service import *
import logging

logger = logging.getLogger(__name__)

medicine_bp = Blueprint('medicine_bp', __name__, url_prefix='/api/medicines')



@medicine_bp.route('', methods=['GET'])
@jwt_required()
def get_medicines():
    """GET /api/medicines - Lista todas las medicinas"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        active_only_str = request.args.get('active_only', 'false').lower()
        get_all_str = request.args.get('get_all', 'false').lower()
        active_only = active_only_str in ['true', '1', 'yes', 'on']
        get_all = get_all_str in ['true', '1', 'yes', 'on']
        print(f"🔍 URL: {request.url}")
        print(f"🔍 active_only_str='{active_only_str}' -> active_only={active_only}")
        
        medicines = get_all_medicines(active_only)
        medicines = sorted(medicines, key=lambda m: m.id)
        total = len(medicines)
        if(get_all):
            return jsonify({
            'medicines': [m.to_dict() for m in medicines],
            'pagination': {
                'page': page,
                'pages': total,
                'per_page': total,
                'total': total
            }
        })

        start = (page - 1) * per_page
        end = start + per_page
        paginated_items = medicines[start:end]
        
        return jsonify({
            'medicines': [m.to_dict() for m in paginated_items],
            'pagination': {
                'page': page,
                'pages': (total + per_page - 1) // per_page,
                'per_page': per_page,
                'total': total
            }
        })
    except Exception as e:
        logger.error(f"Error al obtener medicinas: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@medicine_bp.route('/<int:medicine_id>', methods=['GET'])
@jwt_required()
def get_medicine(medicine_id):
    """GET /api/medicines/:id - Obtener medicina por ID"""
    medicine = Medicine.query.get_or_404(medicine_id)
    return jsonify(medicine.to_dict(include_sensitive=True))

@medicine_bp.route('', methods=['POST'])
@jwt_required()
def create_medicine():
    """POST /api/medicines - Crear nueva medicina"""
    try:
        data = request.get_json()
        medicine = Medicine(**data)
        db.session.add(medicine)
        db.session.commit()
        return jsonify(medicine.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando medicina: {str(e)}")
        return jsonify({'error': 'Error al crear medicina'}), 400

@medicine_bp.route('/<int:medicine_id>', methods=['PUT'])
@jwt_required()
def update_medicine(medicine_id):
    """PUT /api/medicines/:id - Actualizar medicina"""
    medicine = Medicine.query.get_or_404(medicine_id)
    data = request.get_json()
    
    for key, value in data.items():
        setattr(medicine, key, value)
    
    medicine.updated_at = db.func.now()
    db.session.commit()
    return jsonify(medicine.to_dict())

@medicine_bp.route('enable/<int:medicine_id>', methods=['PUT'])
@jwt_required()
def enable_medicine(medicine_id):
    """PUT /api/medicines/:id - Actualizar medicina"""
    medicine = Medicine.query.get_or_404(medicine_id)    
    medicine.is_active = True
    db.session.commit()
    return jsonify(medicine.to_dict())

@medicine_bp.route('disable/<int:medicine_id>', methods=['PUT'])
@jwt_required()
def disable_medicine(medicine_id):
    """PUT /api/medicines/:id - Actualizar medicina"""
    medicine = Medicine.query.get_or_404(medicine_id)    
    medicine.is_active = False
    db.session.commit()
    return jsonify(medicine.to_dict())

@medicine_bp.route('/<int:medicine_id>', methods=['DELETE'])
@jwt_required()
def delete_medicine(medicine_id):
    """DELETE /api/medicines/:id - Eliminar medicina"""
    medicine = Medicine.query.get_or_404(medicine_id)
    db.session.delete(medicine)
    db.session.commit()
    return jsonify({'message': 'Medicina eliminada'})


@medicine_bp.route('/patients/<int:patient_id>/medicines', methods=['GET'])
@jwt_required()
def get_patient_medicines(patient_id):
    """GET /api/medicines/patients/:patient_id/medicines"""        
    medicines = db.session.query(
        Medicine, 
        patient_medicines.c.dose_per_take, 
        patient_medicines.c.notes
    ).join(
        patient_medicines,
        (patient_medicines.c.medicine_id == Medicine.id) & 
        (patient_medicines.c.patient_id == patient_id)
    ).filter(Medicine.is_active == True).all()        
    result = []
    for medicine_row, dose_per_take, notes in medicines:
        medicine_data = medicine_row.to_dict()
        medicine_data['dose_per_take'] = dose_per_take or '1'
        medicine_data['notes'] = notes or ''
        result.append(medicine_data)
    
    return jsonify({
        'medicines': result
    })

@medicine_bp.route('/patients/<int:patient_id>/medicines/<int:medicine_id>', methods=['POST', 'PUT'])
@jwt_required()
def assign_medicine_to_patient(patient_id, medicine_id):
    data = request.get_json() or {}
    dose_per_take = data.get('dose_per_take', '1')
    notes = data.get('notes', '')
        
    existing = db.session.query(patient_medicines).filter_by(
        patient_id=patient_id, 
        medicine_id=medicine_id
    ).first()
    
    if existing:        
        stmt = (
            patient_medicines.update()
            .where(patient_medicines.c.patient_id == patient_id)
            .where(patient_medicines.c.medicine_id == medicine_id)
            .values(dose_per_take=dose_per_take, notes=notes)
        )
        db.session.execute(stmt)
    else:        
        stmt = patient_medicines.insert().values(
            patient_id=patient_id,
            medicine_id=medicine_id,
            dose_per_take=dose_per_take,
            notes=notes
        )
        db.session.execute(stmt)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Medicina asignada/actualizada correctamente',
        'medicine_id': medicine_id,
        'dose_per_take': dose_per_take,
        'notes': notes
    }), 201

@medicine_bp.route('/patients/<int:patient_id>/medicines/<int:medicine_id>', methods=['DELETE'])
@jwt_required()
def remove_medicine_from_patient(patient_id, medicine_id):
    """DELETE /api/medicines/patients/:patient_id/medicines/:medicine_id - Quitar medicina"""
        
    stmt = patient_medicines.delete().where(
        patient_medicines.c.patient_id == patient_id,
        patient_medicines.c.medicine_id == medicine_id
    )
    
    result = db.session.execute(stmt)
    db.session.commit()
        
    if result.rowcount == 0:
        return jsonify({'error': 'Asignación no encontrada'}), 404
    
    return jsonify({'message': 'Medicina removida correctamente'}), 200

@medicine_bp.route('/patients/<int:patient_id>/medicines/bulk-delete', methods=['DELETE'])
@jwt_required()
def bulk_remove_medicines(patient_id):
    """DELETE /api/medicines/patients/:patient_id/medicines/bulk-delete"""
    data = request.get_json() or {}
    medicine_ids = data.get('medicine_ids', [])
    
    if not medicine_ids:
        return jsonify({'error': 'No se enviaron IDs'}), 400
    
    stmt = patient_medicines.delete().where(
        patient_medicines.c.patient_id == patient_id,
        patient_medicines.c.medicine_id.in_(medicine_ids)
    )
    
    result = db.session.execute(stmt)
    db.session.commit()
    
    return jsonify({
        'message': f'Eliminados {result.rowcount} medicamentos'
    }), 200
    
@medicine_bp.route('/search', methods=['GET'])
@jwt_required()
def search_medicines():
    """GET /api/medicines/search?q=paracetamol&active_only=true"""
    query = request.args.get('q', '')
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    medicines = Medicine.query.filter(
        Medicine.name.ilike(f'%{query}%')
    )
    
    if active_only:
        medicines = medicines.filter(Medicine.is_active == True)
    
    return jsonify({
        'medicines': [m.to_dict() for m in medicines.limit(20).all()],
        'count': medicines.count()
    })


@medicine_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Medicina no encontrada'}), 404

@medicine_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Solicitud inválida'}), 400

@medicine_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500
