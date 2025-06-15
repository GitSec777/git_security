# organization.py

from flask import Blueprint, request, jsonify, session
from services.getReq import (
    get_org_members,
    get_org_no_mfa_members,
    get_repo_admin_members,
    get_repos,
    get_public_members,
    get_filtered_org_data
)
# hi

org_bp = Blueprint('org', __name__)

# Existing routes
@org_bp.route('/org/members', methods=['GET'])
def get_org_members():
    org = request.args.get('org')
    token = session.get('github_token')  # Retrieve token from session
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    response = get_org_members(org, token)
    return jsonify(response)

@org_bp.route('/org/members/no_mfa', methods=['GET'])
def get_org_no_mfa_members_route():
    org = request.args.get('org')
    token = session.get('github_token')  # Retrieve token from session
    print("token:", token)
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    response = get_org_no_mfa_members(org, token)
    return jsonify(response)

@org_bp.route('/org/members/admin', methods=['GET'])
def get_org_admin_members_route():
    org = request.args.get('org')
    token = session.get('github_token')  # Retrieve token from session
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    response = get_repo_admin_members(org, token)
    return jsonify(response)

@org_bp.route('/org/repos', methods=['GET'])
def get_org_repos_route():
    org = request.args.get('org')
    token = session.get('github_token')  # Retrieve token from session
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    response = get_repos(org, token)
    return jsonify(response)

@org_bp.route('/org/public_members', methods=['GET'])
def get_public_members_route():
    org = request.args.get('org')
    token = session.get('github_token')  # Retrieve token from session
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    response = get_public_members(org, token)
    return jsonify(response)

# New route for filtered org data
@org_bp.route('/org/<org_name>', methods=['GET'])
def get_filtered_org_data_route(org_name):
    token = session.get('github_token')  # Retrieve token from session
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    filtered_data = get_filtered_org_data(org_name, token)
    if 'error' in filtered_data:
        return jsonify({'error': filtered_data['error']}), 400
    return jsonify(filtered_data)
