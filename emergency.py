from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import EmergencyReport
from app.utils.decorators import vet_required
from app import db

bp = Blueprint('emergency', __name__)

@bp.route('/emergency', methods=['POST'])
@jwt_required()
def create_emergency_report():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_report = EmergencyReport(
        user_id=user_id,
        emergency_type=data.get('emergency_type'),
        description=data.get('description'),
        location=data.get('location'),
        status='pending'
    )
    
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify({
        "msg": "Emergency report created successfully",
        "report": {
            "id": new_report.id,
            "emergency_type": new_report.emergency_type,
            "description": new_report.description,
            "location": new_report.location,
            "status": new_report.status
        }
    }), 201

@bp.route('/emergency/<int:report_id>', methods=['PUT'])
@vet_required()
def update_emergency_status(report_id):
    report = EmergencyReport.query.get(report_id)
    if not report:
        return jsonify({"msg": "Emergency report not found"}), 404
    
    data = request.get_json()
    
    report.status = data.get('status', report.status)
    
    db.session.commit()
    
    return jsonify({
        "msg": "Emergency report updated successfully",
        "report": {
            "id": report.id,
            "emergency_type": report.emergency_type,
            "description": report.description,
            "location": report.location,
            "status": report.status
        }
    })

@bp.route('/emergency', methods=['GET'])
@jwt_required()
def get_emergency_reports():
    user_id = get_jwt_identity()
    reports = EmergencyReport.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        "id": report.id,
        "emergency_type": report.emergency_type,
        "description": report.description,
        "location": report.location,
        "status": report.status,
        "created_at": report.created_at.isoformat()
    } for report in reports])

@bp.route('/emergency/pending', methods=['GET'])
@vet_required()
def get_pending_emergencies():
    reports = EmergencyReport.query.filter_by(status='pending').all()
    
    return jsonify([{
        "id": report.id,
        "emergency_type": report.emergency_type,
        "description": report.description,
        "location": report.location,
        "status": report.status,
        "created_at": report.created_at.isoformat()
    } for report in reports])