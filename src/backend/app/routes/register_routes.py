from .user_routes import user_bp
from .auth_routes import auth_bp
from .patients_routes import patient_bp
from .medicine_routes import medicine_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(medicine_bp)
