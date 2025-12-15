from functools import wraps
import logging
from flask import Blueprint, request, jsonify
from app.models.user import *
from app.services.auth_service import register_user,login_user
from app.services.user_service import get_user_by_id
from app.extensions import db
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, create_access_token, jwt_required, get_jwt_identity

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')


def token_required(f):
    """Decorador para rutas que requieren autenticación con Flask-JWT-Extended"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            request.current_user = user_identity
            
        except Exception as e:
            return jsonify({"msg": "Token inválido o faltante", "error": str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorador para rutas que requieren permisos de admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            if not current_user.get('is_admin', False):
                return jsonify({'error': 'Permisos de administrador requeridos'}), 403
            
            request.current_user = current_user
            
        except Exception as e:
            return jsonify({"msg": "Token inválido o faltante", "error": str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

    
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'Campos requeridos: {", ".join(missing_fields)}'}), 400

    
        user, token, message = register_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )

        if not user:
            return jsonify({'error': message}), 400

    
        token = create_access_token(identity={
            'user_id': user.id,
            'username': user.username,
            'is_admin': user.is_admin
        })

        return jsonify({
            'message': message,
            'user': user.to_dict(),
            'token': token
        }), 201

    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        identifier = data.get('username') or data.get('email')
        password = data.get('password')
        if not identifier or not password:
            return jsonify({'error': 'Username/email y password son requeridos'}), 400
        user, token, message = login_user(identifier, password)
        if not user:
            return jsonify({'error': message}), 401
        return jsonify({
            'message': message,
            'user': user.to_dict(include_sensitive=True),
            'token': token
        })

    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_identity = get_jwt_identity()
    user = get_user_by_id(current_user_identity);
    return jsonify(user.to_dict(include_sensitive=True))


@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_identity = get_jwt_identity()
        data = request.json
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        forbidden_fields = ['username', 'password', 'is_admin', 'is_active']
        for field in forbidden_fields:
            data.pop(field, None)

        user, message = update_profile_service(current_user_identity['user_id'], data)
        if not user:
            return jsonify({'error': message}), 400

        return jsonify({
            'message': message,
            'user': user.to_dict(include_sensitive=True)
        })

    except Exception as e:
        logger.error(f"Error al actualizar perfil: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_identity = get_jwt_identity()
        data = request.json
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({'error': 'Contraseña actual y nueva son requeridas'}), 400

        success, message = change_password(
            current_user_identity['user_id'],
            current_password,
            new_password
        )

        if not success:
            return jsonify({'error': message}), 400

        return jsonify({'message': message})

    except Exception as e:
        logger.error(f"Error al cambiar contraseña: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    

@auth_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@auth_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Solicitud inválida'}), 400

@auth_bp.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'No autorizado'}), 401

@auth_bp.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Prohibido - permisos insuficientes'}), 403

@auth_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500