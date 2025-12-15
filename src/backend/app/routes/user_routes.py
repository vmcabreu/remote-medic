from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.user_service import *
from .auth_routes import admin_required
import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')

#Consigue una lista de usuarios
@user_bp.route('/', methods=['GET'])
@admin_required
@jwt_required()
def list_users(current_user):
    """GET /api/users - Listar todos los usuarios (solo admin)"""
    try:
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)
        
        if not page and not per_page:
            users = get_all_users()
            return jsonify({
                'users': [u.to_dict(include_sensitive=True) for u in users],
                'total': len(users)
            })
        
        page = page or 1
        per_page = per_page or 10
        
        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({'error': 'Parámetros de paginación inválidos'}), 400
        
        paginated_users = get_users_paginated(page, per_page)
        
        return jsonify({
            'users': [u.to_dict(include_sensitive=True) for u in paginated_users.items],
            'pagination': {
                'page': paginated_users.page,
                'pages': paginated_users.pages,
                'per_page': paginated_users.per_page,
                'total': paginated_users.total,
                'has_next': paginated_users.has_next,
                'has_prev': paginated_users.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Error al obtener usuarios: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@admin_required
@jwt_required()
def get_user(current_user, user_id):
    """GET /api/users/<id> - Obtener usuario por ID (solo admin)"""
    try:
        user = get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({'user': user.to_dict(include_sensitive=True)})
        
    except Exception as e:
        logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@user_bp.route('/<int:user_id>/activate', methods=['POST'])
@admin_required
@jwt_required()
def activate_user(current_user, user_id):
    """POST /api/users/<id>/activate - Activar usuario (solo admin)"""
    try:
        success, message = activate_user(user_id)
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({'message': message})
        
    except Exception as e:
        logger.error(f"Error al activar usuario {user_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@user_bp.route('/<int:user_id>/deactivate', methods=['POST'])
@admin_required
@jwt_required()
def deactivate_user(current_user, user_id):
    """POST /api/users/<id>/deactivate - Desactivar usuario (solo admin)"""
    try:
        if user_id == current_user.id:
            return jsonify({'error': 'No puedes desactivar tu propia cuenta'}), 400
        
        success, message = deactivate_user(user_id)
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({'message': message})
        
    except Exception as e:
        logger.error(f"Error al desactivar usuario {user_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@user_bp.errorhandler(404)
def not_found_users(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@user_bp.errorhandler(401)
def unauthorized_users(error):
    return jsonify({'error': 'No autorizado'}), 401

@user_bp.errorhandler(403)
def forbidden_users(error):
    return jsonify({'error': 'Prohibido - permisos insuficientes'}), 403

@user_bp.errorhandler(500)
def internal_error_users(error):
    return jsonify({'error': 'Error interno del servidor'}), 500
