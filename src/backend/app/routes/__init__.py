from .patients_routes import patient_bp, user_patients_bp, carer_bp
from .user_routes import user_bp  

def register_routes(app):
    app.register_blueprint(patient_bp)       
    app.register_blueprint(user_patients_bp) 
    app.register_blueprint(carer_bp)         
    app.register_blueprint(user_bp)           
