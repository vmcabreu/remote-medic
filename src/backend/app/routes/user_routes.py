from flask import Blueprint, request, jsonify
from app.services.user_service import get_all_users, create_user

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
def list_users():
    return jsonify([u.to_dict() for u in get_all_users()])

@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.json
    user = create_user(data['username'], data['email'])
    return jsonify(user.to_dict()), 201
