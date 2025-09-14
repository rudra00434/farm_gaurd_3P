from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import ComplianceRecord
from app.utils.decorators import farmer_required, admin_required
from app import db

bp = Blueprint('compliance', __name__)

@bp.route('/compliance', methods=['POST'])
@farmer_required()
def create_compliance_record():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_record = ComplianceRecord(
        user_id=user_id,
        regulation_type=data.get('regulation_type'),
        status=data.get('status', 'non-compliant'),
        notes=data.get('notes')
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify({
        "msg": "Compliance record created successfully",
        "record": {
            "id": new_record.id,
            "regulation_type": new_record.regulation_type,
            "status": new_record.status,
            "notes": new_record.notes
        }
    }), 201

@bp.route('/compliance/<int:record_id>', methods=['PUT'])
@admin_required()
def update_compliance_status(record_id):
    record = ComplianceRecord.query.get(record_id)
    if not record:
        return jsonify({"msg": "Compliance record not found"}), 404
    
    data = request.get_json()
    
    record.status = data.get('status', record.status)
    record.notes = data.get('notes', record.notes)
    
    db.session.commit()
    
    return jsonify({
        "msg": "Compliance record updated successfully",
        "record": {
            "id": record.id,
            "regulation_type": record.regulation_type,
            "status": record.status,
            "notes": record.notes
        }
    })

@bp.route('/compliance', methods=['GET'])
@jwt_required()
def get_compliance_records():
    user_id = get_jwt_identity()
    records = ComplianceRecord.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        "id": record.id,
        "regulation_type": record.regulation_type,
        "status": record.status,
        "notes": record.notes,
        "created_at": record.created_at.isoformat()
    } for record in records])

@bp.route('/compliance/summary', methods=['GET'])
@admin_required()
def get_compliance_summary():
    records = ComplianceRecord.query.all()
    
    summary = {
        "total": len(records),
        "compliant": len([r for r in records if r.status == 'compliant']),
        "non_compliant": len([r for r in records if r.status == 'non-compliant'])
    }
    
    return jsonify(summary)