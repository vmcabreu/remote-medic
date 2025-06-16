from flask import Blueprint, request, jsonify
from app.services.patients_service import *
import logging

logger = logging.getLogger(__name__)

# Crear el blueprint
patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patients')

# ==========================================
# RUTAS BÁSICAS DE PACIENTES
# ==========================================

@patient_bp.route('/', methods=['GET'])
def list_patients():
    """GET /api/patients - Obtener todos los pacientes (con paginación opcional)"""
    try:
        # Parámetros de paginación opcionales
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)
        
        # Si no hay parámetros de paginación, devolver todos
        if not page and not per_page:
            patients = get_all_patient()
            return jsonify({
                'patients': [p.to_dict() for p in patients],
                'total': len(patients)
            })
        
        # Con paginación
        page = page or 1
        per_page = per_page or 10
        
        # Validar parámetros
        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({'error': 'Parámetros de paginación inválidos'}), 400
        
        paginated_patients = get_patients_paginated(page, per_page)
        
        return jsonify({
            'patients': [p.to_dict() for p in paginated_patients.items],
            'pagination': {
                'page': paginated_patients.page,
                'pages': paginated_patients.pages,
                'per_page': paginated_patients.per_page,
                'total': paginated_patients.total,
                'has_next': paginated_patients.has_next,
                'has_prev': paginated_patients.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Error al obtener pacientes: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@patient_bp.route('/', methods=['POST'])
def add_patient():
    """POST /api/patients - Crear un nuevo paciente"""
    try:
        data = request.json
        
        if not data or 'name' not in data:
            return jsonify({'error': 'El campo name es requerido'}), 400
        
        # Crear el paciente
        new_patient = create_patient(data)
        
        return jsonify({
            'message': 'Paciente creado exitosamente',
            'patient': new_patient.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error al crear paciente: {str(e)}")
        return jsonify({'error': 'Error al crear el paciente'}), 500

@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """GET /api/patients/<id> - Obtener un paciente por ID"""
    try:
        patient = get_patient_by_id(patient_id)
        
        if not patient:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        return jsonify({'patient': patient.to_dict()})
        
    except Exception as e:
        logger.error(f"Error al obtener paciente {patient_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient_route(patient_id):
    """PUT /api/patients/<id> - Actualizar un paciente"""
    try:
        if not patient_exists(patient_id):
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        data = request.json
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        updated_patient = update_patient(patient_id, data)
        
        if not updated_patient:
            return jsonify({'error': 'Error al actualizar el paciente'}), 500
        
        return jsonify({
            'message': 'Paciente actualizado exitosamente',
            'patient': updated_patient.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error al actualizar paciente {patient_id}: {str(e)}")
        return jsonify({'error': 'Error al actualizar el paciente'}), 500

@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient_route(patient_id):
    """DELETE /api/patients/<id> - Eliminar un paciente"""
    try:
        if not patient_exists(patient_id):
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        success = delete_patient(patient_id)
        
        if success:
            return jsonify({'message': 'Paciente eliminado exitosamente'})
        else:
            return jsonify({'error': 'Error al eliminar el paciente'}), 500
            
    except Exception as e:
        logger.error(f"Error al eliminar paciente {patient_id}: {str(e)}")
        return jsonify({'error': 'Error al eliminar el paciente'}), 500

# ==========================================
# RUTAS DE ASIGNACIONES
# ==========================================

@patient_bp.route('/<int:patient_id>/assign', methods=['POST'])
def assign_patient_to_user_route(patient_id):
    """POST /api/patients/<id>/assign - Asignar paciente a usuario"""
    try:
        if not patient_exists(patient_id):
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        data = request.json
        user_id = data.get('user_id') if data else None
        
        if not user_id:
            return jsonify({'error': 'user_id es requerido'}), 400
        
        success = assign_patient_to_user(user_id, patient_id)
        
        if success:
            return jsonify({'message': 'Paciente asignado exitosamente'})
        else:
            return jsonify({'error': 'Error al asignar paciente. Verifique que el usuario existe'}), 400
            
    except Exception as e:
        logger.error(f"Error al asignar paciente {patient_id}: {str(e)}")
        return jsonify({'error': 'Error al asignar el paciente'}), 500

@patient_bp.route('/<int:patient_id>/assign', methods=['DELETE'])
def remove_patient_assignment_route(patient_id):
    """DELETE /api/patients/<id>/assign - Remover asignación de paciente"""
    try:
        if not patient_exists(patient_id):
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        data = request.json
        user_id = data.get('user_id') if data else None
        
        if not user_id:
            return jsonify({'error': 'user_id es requerido'}), 400
        
        success = remove_patient_from_user(user_id, patient_id)
        
        if success:
            return jsonify({'message': 'Asignación removida exitosamente'})
        else:
            return jsonify({'error': 'Error al remover asignación'}), 400
            
    except Exception as e:
        logger.error(f"Error al remover asignación del paciente {patient_id}: {str(e)}")
        return jsonify({'error': 'Error al remover la asignación'}), 500

@patient_bp.route('/<int:patient_id>/users', methods=['GET'])
def get_patient_users_route(patient_id):
    """GET /api/patients/<id>/users - Obtener usuarios asignados al paciente"""
    try:
        if not patient_exists(patient_id):
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        users = get_patient_users(patient_id)
        
        return jsonify({
            'patient_id': patient_id,
            'assigned_users': [u.to_dict() for u in users],
            'total_users': len(users)
        })
        
    except Exception as e:
        logger.error(f"Error al obtener usuarios del paciente {patient_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ==========================================
# RUTAS ADICIONALES PARA USUARIOS/CUIDADORES
# ==========================================

# Crear blueprint adicional para rutas de usuarios con pacientes
user_patients_bp = Blueprint('user_patients_bp', __name__, url_prefix='/api/users')

@user_patients_bp.route('/<int:user_id>/patients', methods=['GET'])
def get_user_patients_route(user_id):
    """GET /api/users/<id>/patients - Obtener pacientes asignados al usuario"""
    try:
        patients = get_user_patients(user_id)
        
        if patients is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'user_id': user_id,
            'patients': [p.to_dict() for p in patients],
            'total_patients': len(patients)
        })
        
    except Exception as e:
        logger.error(f"Error al obtener pacientes del usuario {user_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# Blueprint para cuidadores
carer_bp = Blueprint('carer_bp', __name__, url_prefix='/api/carers')

@carer_bp.route('/<int:carer_id>/patients', methods=['GET'])
def get_carer_patients_route(carer_id):
    """GET /api/carers/<id>/patients - Obtener pacientes del cuidador"""
    try:
        # Usar get_user_patients ya que get_patient_by_carer_id tiene un bug
        patients = get_user_patients(carer_id)
        
        if patients is None:
            return jsonify({'error': 'Cuidador no encontrado'}), 404
        
        return jsonify({
            'carer_id': carer_id,
            'patients': [p.to_dict() for p in patients],
            'total_patients': len(patients)
        })
        
    except Exception as e:
        logger.error(f"Error al obtener pacientes del cuidador {carer_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ==========================================
# MANEJADORES DE ERRORES
# ==========================================

@patient_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@patient_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Solicitud inválida'}), 400

@patient_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# Aplicar los mismos manejadores a los otros blueprints
@user_patients_bp.errorhandler(404)
def not_found_users(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@user_patients_bp.errorhandler(500)
def internal_error_users(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@carer_bp.errorhandler(404)
def not_found_carers(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@carer_bp.errorhandler(500)
def internal_error_carers(error):
    return jsonify({'error': 'Error interno del servidor'}), 500
