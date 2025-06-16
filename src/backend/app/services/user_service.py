from app.models.user import User, db
from datetime import datetime
from flask import current_app

def get_all_users():
    """Obtener todos los usuarios"""
    return User.query.all()

def get_user_by_id(user_id):
    """Obtener usuario por ID"""
    return User.query.get(user_id)

def get_user_by_username(username):
    """Obtener usuario por username"""
    return User.query.filter_by(username=username.lower()).first()

def get_user_by_email(email):
    """Obtener usuario por email"""
    return User.query.filter_by(email=email.lower()).first()

def get_active_users():
    """Obtener usuarios activos"""
    return User.query.filter_by(is_active=True).all()

def get_users_paginated(page=1, per_page=10):
    """Obtener usuarios paginados"""
    return User.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def user_exists(user_id):
    """Verificar si existe un usuario"""
    return User.query.get(user_id) is not None

def delete_user(user_id):
    """Eliminar usuario (soft delete - desactivar)"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False
        
        # Soft delete - solo desactivar
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar usuario: {str(e)}")
        return False
