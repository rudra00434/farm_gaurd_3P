from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.models import User
from app.services.firebase_service import verify_firebase_token
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Verify Firebase token
    id_token = data.get('idToken')
    firebase_user = verify_firebase_token(id_token)
    
    if not firebase_user:
        return jsonify({"msg": "Invalid Firebase token"}), 401
    
    # Check if user already exists
    existing_user = User.query.filter_by(firebase_uid=firebase_user['uid']).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 400
    
    # Create new user
    new_user = User(
        firebase_uid=firebase_user['uid'],
        email=firebase_user['email'],
        name=data.get('name'),
        role=data.get('role', 'farmer')  # Default role is farmer
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Create JWT token
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({
        "msg": "User registered successfully",
        "access_token": access_token,
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name,
            "role": new_user.role
        }
    }), 201

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Verify Firebase token
    id_token = data.get('idToken')
    firebase_user = verify_firebase_token(id_token)
    
    if not firebase_user:
        return jsonify({"msg": "Invalid Firebase token"}), 401
    
    # Get user from database
    user = User.query.filter_by(firebase_uid=firebase_user['uid']).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    # Create JWT token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "msg": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    })