from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.models import User

def admin_required():
    """Decorator to check if user is an admin"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user.role != 'admin':
                return jsonify({"msg": "Admins only!"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def vet_required():
    """Decorator to check if user is a vet"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user.role != 'vet':
                return jsonify({"msg": "Vets only!"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def farmer_required():
    """Decorator to check if user is a farmer"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user.role != 'farmer':
                return jsonify({"msg": "Farmers only!"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper