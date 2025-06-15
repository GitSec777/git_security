from flask import Blueprint, jsonify, session
from services.getReq import (
    get_repo_code_scanning_alerts,
    get_repo_secret_scanning_alerts,
    get_repo_vul_alerts
)

repo_routes = Blueprint('repo_routes', __name__)

@repo_routes.route('/api/repos/<org>/<repo>/code-scanning/alerts', methods=['GET'])
def code_scanning_alerts(org, repo):
    """Get code scanning alerts for a specific repository"""
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    alerts = get_repo_code_scanning_alerts(org, repo, token)
    
    if alerts is None:
        return jsonify({'error': 'Failed to fetch code scanning alerts'}), 400
        
    return jsonify(alerts)

@repo_routes.route('/api/repos/<org>/<repo>/secret-scanning/alerts', methods=['GET'])
def secret_scanning_alerts(org, repo):
    """Get secret scanning alerts for a specific repository"""
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    alerts = get_repo_secret_scanning_alerts(org, repo, token)
    
    if alerts is None:
        return jsonify({'error': 'Failed to fetch secret scanning alerts'}), 400
        
    return jsonify(alerts)

@repo_routes.route('/api/repos/<org>/<repo>/vulnerability-alerts', methods=['GET'])
def vulnerability_alerts(org, repo):
    """Get vulnerability alerts for a specific repository"""
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    token = session['github_token']
    alerts = get_repo_vul_alerts(org, repo, token)
    
    if alerts is None:
        return jsonify({'error': 'Failed to fetch vulnerability alerts'}), 400
        
    return jsonify(alerts)
