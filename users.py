from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import User
from app.utils.decorators import admin_required
from app import db

bp = Blueprint('users', __name__)

@bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role
    })

@bp.route('/users', methods=['GET'])
@admin_required()
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role
    } for user in users])

@bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    data = request.get_json()
    
    if 'role' in data:
        user.role = data['role']
    if 'name' in data:
        user.name = data['name']
    
    db.session.commit()
    
    return jsonify({
        "msg": "User updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    })