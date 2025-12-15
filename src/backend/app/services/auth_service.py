from app.models.user import User, db
from flask import current_app
import re
from datetime import datetime, timedelta

@staticmethod
def register_user(username, email, password, first_name=None, last_name=None):
    """Registrar nuevo usuario"""
    try:
        if not validate_username(username):
            return None, "Nombre de usuario inválido"
        
        if not validate_email(email):
            return None, "Email inválido"
        
        if not validate_password(password):
            return None, "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número"
        
        
        if User.query.filter_by(username=username).first():
            return None, "El nombre de usuario ya existe"
        
        if User.query.filter_by(email=email).first():
            return None, "El email ya está registrado"
        
        user = User(
            username=username.lower().strip(),
            email=email.lower().strip(),
            first_name=first_name.strip() if first_name else None,
            last_name=last_name.strip() if last_name else None
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, "Usuario registrado exitosamente"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al registrar usuario: {str(e)}")
        return None, "Error interno del servidor"

@staticmethod
def login_user(identifier, password):
    """Login de usuario (por username o email)"""
    try:
        user = User.query.filter(
            (User.username == identifier.lower()) | 
            (User.email == identifier.lower())
        ).first()
        
        if not user:
            return None, None, "Usuario no encontrado"
        
        if not user.is_active:
            return None, None, "Cuenta desactivada"
        
        if not user.check_password(password):
            return None, None, "Contraseña incorrecta"
        
        user.update_last_login()
        token = user.generate_token()
        return user, token, "Login exitoso"
        
    except Exception as e:
        current_app.logger.error(f"Error en login: {str(e)}")
        return None, None, "Error interno del servidor"

@staticmethod
def change_password(user_id, current_password, new_password):
    """Cambiar contraseña"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return False, "Usuario no encontrado"
        
        if not user.check_password(current_password):
            return False, "Contraseña actual incorrecta"
        
        if not validate_password(new_password):
            return False, "La nueva contraseña no cumple los requisitos"
        
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return True, "Contraseña actualizada exitosamente"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al cambiar contraseña: {str(e)}")
        return False, "Error interno del servidor"

@staticmethod
def update_profile(user_id, data):
    """Actualizar perfil de usuario"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return None, "Usuario no encontrado"
        
        
        if 'email' in data and data['email'] != user.email:
            if not validate_email(data['email']):
                return None, "Email inválido"
            
            if User.query.filter_by(email=data['email']).first():
                return None, "El email ya está registrado"
            
            user.email = data['email'].lower().strip()
        
        
        if 'first_name' in data:
            user.first_name = data['first_name'].strip() if data['first_name'] else None
        
        if 'last_name' in data:
            user.last_name = data['last_name'].strip() if data['last_name'] else None
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return user, "Perfil actualizado exitosamente"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar perfil: {str(e)}")
        return None, "Error interno del servidor"

@staticmethod
def validate_username(username):
    """Validar nombre de usuario"""
    if not username or len(username) < 3 or len(username) > 64:
        return False
    
    
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None

@staticmethod
def validate_email(email):
    """Validar email"""
    if not email or len(email) > 120:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@staticmethod
def validate_password(password):
    """Validar contraseña"""
    if not password or len(password) < 8:
        return False
    
    
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    
    return has_upper and has_lower and has_digit

@staticmethod
def get_user_by_token(token):
    """Obtener usuario por token"""
    return User.verify_token(token)

@staticmethod
def deactivate_user(user_id):
    """Desactivar usuario"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False, "Usuario no encontrado"
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return True, "Usuario desactivado"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al desactivar usuario: {str(e)}")
        return False, "Error interno del servidor"

@staticmethod
def activate_user(user_id):
    """Activar usuario"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False, "Usuario no encontrado"
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return True, "Usuario activado"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al activar usuario: {str(e)}")
        return False, "Error interno del servidor"
