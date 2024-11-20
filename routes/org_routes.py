from flask import Blueprint, jsonify, request, session
from services.getReq import (
    get_repo_no_mfa_members,
    get_repo_admin_members,
    get_dependabot_alerts,
    get_repo_report
)

org_routes = Blueprint('org_routes', __name__)

@org_routes.route('/api/org/<org>/no-mfa-members', methods=['GET'])
def no_mfa_members(org):
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    token = session['github_token']
    members = get_repo_no_mfa_members(org, token)
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