from flask import Blueprint, jsonify, request, session
from services.getReq import (
    get_org_no_mfa_members,
    get_repo_admin_members,
    get_dependabot_alerts,
    get_repo_report,
    get_org_dependebot_alerts,
    get_org_security_advisories,
    get_org_repo_creation_settings
)

org_routes = Blueprint('org_routes', __name__)

@org_routes.route('/api/org/<org>/no-mfa-members', methods=['GET'])
def no_mfa_members(org):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    token = session['github_token']
    members = get_org_no_mfa_members(org, token)
    return jsonify(members)

@org_routes.route('/api/org/<org>/admin-members', methods=['GET'])
def admin_members(org):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    admins = get_repo_admin_members(org, token)
    return jsonify(admins)

@org_routes.route('/api/repos/<org>/<repo>/dependabot-alerts', methods=['GET'])
def dependabot_alerts(org, repo):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    alerts = get_dependabot_alerts(org, repo, token)
    return jsonify(alerts)

@org_routes.route('/api/repos/<org>/<repo>/report', methods=['GET'])
def repo_report(org, repo):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    report = get_repo_report(f"{org}/{repo}", token)
    return jsonify(report)

@org_routes.route('/api/org/<org>/dependebot-alerts', methods=['GET'])
def org_dependebot_alerts(org):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    insights = get_org_dependebot_alerts(org, token)
    return jsonify(insights or {})

@org_routes.route('/api/org/<org>/security-advisories', methods=['GET'])
def org_security_advisories(org):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    advisories = get_org_security_advisories(org, token)
    return jsonify(advisories or {})

@org_routes.route('/api/org/<org>/repo-settings', methods=['GET'])
def org_repo_settings(org):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    settings = get_org_repo_creation_settings(org, token)
    return jsonify(settings or {}) 
