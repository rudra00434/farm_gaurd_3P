import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models.models import Disease
from app import db
from app.utils.decorators import farmer_required, vet_required

bp = Blueprint('disease', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath
    return None

@bp.route('/diseases', methods=['POST'])
@farmer_required()
def create_disease_report():
    user_id = get_jwt_identity()
    
    if 'image' not in request.files:
        return jsonify({"msg": "No image file"}), 400
        
    file = request.files['image']
    image_path = save_image(file)
    
    if not image_path:
        return jsonify({"msg": "Invalid file type"}), 400
    
    data = request.form
    
    new_disease = Disease(
        user_id=user_id,
        animal_type=data.get('animal_type'),
        symptoms=data.get('symptoms'),
        image_url=image_path
    )
    
    db.session.add(new_disease)
    db.session.commit()
    
    return jsonify({
        "msg": "Disease report created successfully",
        "disease": {
            "id": new_disease.id,
            "animal_type": new_disease.animal_type,
            "symptoms": new_disease.symptoms,
            "image_url": new_disease.image_url,
            "diagnosis": new_disease.diagnosis
        }
    }), 201

@bp.route('/diseases/<int:disease_id>/diagnose', methods=['POST'])
@vet_required()
def diagnose_disease(disease_id):
    disease = Disease.query.get(disease_id)
    if not disease:
        return jsonify({"msg": "Disease report not found"}), 404
    
    data = request.get_json()
    disease.diagnosis = data.get('diagnosis')
    
    db.session.commit()
    
    return jsonify({
        "msg": "Diagnosis added successfully",
        "disease": {
            "id": disease.id,
            "animal_type": disease.animal_type,
            "symptoms": disease.symptoms,
            "image_url": disease.image_url,
            "diagnosis": disease.diagnosis
        }
    })

@bp.route('/diseases', methods=['GET'])
@jwt_required()
def get_diseases():
    user_id = get_jwt_identity()
    user_diseases = Disease.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        "id": disease.id,
        "animal_type": disease.animal_type,
        "symptoms": disease.symptoms,
        "image_url": disease.image_url,
        "diagnosis": disease.diagnosis,
        "created_at": disease.created_at.isoformat()
    } for disease in user_diseases])