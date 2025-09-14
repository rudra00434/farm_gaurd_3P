from app import create_app, db
from app.models.models import User, Disease, ComplianceRecord, EmergencyReport, NetworkPost, NetworkComment

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Disease': Disease,
        'ComplianceRecord': ComplianceRecord,
        'EmergencyReport': EmergencyReport,
        'NetworkPost': NetworkPost,
        'NetworkComment': NetworkComment
    }

if __name__ == '__main__':
    app.run(debug=True)