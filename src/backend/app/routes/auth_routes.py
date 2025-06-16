from functools import wraps
import logging
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.auth_service import get_user_by_token,register_user,login_user
from app.extensions import db
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required, get_jwt_identity

logger = logging.getLogger(__name__)

# Blueprint de autenticación
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

# Blueprint de usuarios (admin)
user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')

# ==========================================
# DECORADOR PARA AUTENTICACIÓN
# ==========================================

def token_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Token en header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token inválido'}), 401
        
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        try:
            current_user = get_user_by_token(token)
            if not current_user:
                return jsonify({'error': 'Token inválido o expirado'}), 401
            
            if not current_user.is_active:
                return jsonify({'error': 'Cuenta desactivada'}), 401
                
        except Exception as e:
            logger.error(f"Error en validación de token: {str(e)}")
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorador para rutas que requieren permisos de admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Token inválido'}), 401
        
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        try:
            current_user = get_user_by_token(token)
            if not current_user or not current_user.is_admin:
                return jsonify({'error': 'Permisos de administrador requeridos'}), 403
                
        except Exception as e:
            logger.error(f"Error en validación de admin: {str(e)}")
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# ==========================================
# RUTAS DE AUTENTICACIÓN
# ==========================================

@auth_bp.route('/register', methods=['POST'])
def register():
    """POST /api/auth/register - Registrar nuevo usuario"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Campos requeridos
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({'error': f'Campos requeridos: {", ".join(missing_fields)}'}), 400
        
        # Registrar usuario
        user, message = register_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        if not user:
            return jsonify({'error': message}), 400
        
        # Generar token para el nuevo usuario
        token = user.generate_token()
        
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
    """POST /api/auth/login - Iniciar sesión"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        identifier = data.get('username') or data.get('email')
        password = data.get('password')
        
        if not identifier or not password:
            return jsonify({'error': 'Username/email y password son requeridos'}), 400
        
        # Intentar login
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
@token_required
def get_current_user(current_user):
    """GET /api/auth/me - Obtener información del usuario actual"""
    return jsonify({
        'user': current_user.to_dict(include_sensitive=True)
    })

@auth_bp.route('/me', methods=['PUT'])
@token_required
def update_profile(current_user):
    """PUT /api/auth/me - Actualizar perfil del usuario actual"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # No permitir cambio de username, password o campos admin
        forbidden_fields = ['username', 'password', 'is_admin', 'is_active']
        for field in forbidden_fields:
            if field in data:
                del data[field]
        
        user, message = update_profile(current_user.id, data)
        
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
@token_required
def change_password(current_user):
    """POST /api/auth/change-password - Cambiar contraseña"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Contraseña actual y nueva son requeridas'}), 400
        
        success, message = change_password(
            current_user.id, 
            current_password, 
            new_password
        )
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({'message': message})
        
    except Exception as e:
        logger.error(f"Error al cambiar contraseña: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    
# ==========================================
# MANEJADORES DE ERRORES
# ==========================================

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