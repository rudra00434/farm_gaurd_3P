import firebase_admin
from firebase_admin import auth, credentials
from flask import current_app

def init_firebase():
    """Initialize Firebase Admin SDK"""
    cred = credentials.Certificate(current_app.config['FIREBASE_CREDENTIALS'])
    firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token):
    """Verify Firebase ID token and return user info"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None

def get_firebase_user(uid):
    """Get Firebase user by UID"""
    try:
        user = auth.get_user(uid)
        return user
    except Exception as e:
        return None