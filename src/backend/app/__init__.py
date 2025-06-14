from flask import Flask,request, jsonify
from .extensions import db
from .routes.register_routes import register_routes  
from datetime import timedelta
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

EXCLUDED_ROUTES = [
    '/auth/login',
    '/auth/refresh'
]

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    app.before_request(jwt_interceptor)

    db.init_app(app)

    register_routes(app) 


    return app

def jwt_interceptor():
    if request.path in EXCLUDED_ROUTES or request.path.startswith('/static'):
        return 
    try:
        verify_jwt_in_request()
    except Exception as e:
        return jsonify({"msg": "Token inválido o faltante", "error": str(e)}), 401