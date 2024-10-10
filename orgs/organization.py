import os
from flask import Blueprint, request, jsonify
from utils.http_helper import send_http_request
from services.getReq import get_repo_members, get_repo_no_mfa_members, get_repo_admin_members, get_repos
import requests

org_bp = Blueprint('org', __name__)

git_token = os.getenv('GITHUB_TOKEN')

# Existing routes
@org_bp.route('/org/members', methods=['GET'])
def get_org_members():
    org = request.args.get('org')
    response = get_repo_members(org, git_token)
    return jsonify(response)

@org_bp.route('/org/members/no_mfa', methods=['GET'])
def get_org_no_mfa_members():
    org = request.args.get('org')
    response = get_repo_no_mfa_members(org, git_token)
    return jsonify(response)

@org_bp.route('/org/members/admin', methods=['GET'])
def get_org_admin_members():
    org = request.args.get('org')
    response = get_repo_admin_members(org, git_token)
    return jsonify(response)

@org_bp.route('/org/repos', methods=['GET'])
def get_org_repos():
    org = request.args.get('org')
    response = get_repos(org, git_token)
    return jsonify(response)

@org_bp.route('/org/public_members', methods=['GET'])
def get_public_members():
    org = request.args.get('org')
    response = get_public_members(org, git_token)
    return jsonify(response)

# New route for filtered org data
@org_bp.route('/org/<org_name>', methods=['GET'])
def get_filtered_org_data_route(org_name):
    filtered_data = get_filtered_org_data(org_name)
    return jsonify(filtered_data)

def get_filtered_org_data(org_name):
    github_data = get_github_data(f"orgs/{org_name}")
    
    # Additional API calls for more detailed information
    members_url = f"https://api.github.com/orgs/{org_name}/members"
    repos_url = f"https://api.github.com/orgs/{org_name}/repos"
    
    members_data = requests.get(members_url, headers=github_data['headers']).json()
    repos_data = requests.get(repos_url, headers=github_data['headers']).json()

    filtered_data = {
        "name": github_data['data'].get('name', ''),
        "login": github_data['data'].get('login', ''),
        "url": github_data['data'].get('url', ''),
        "html_url": github_data['data'].get('html_url', ''),
        "created_at": github_data['data'].get('created_at', ''),
        "updated_at": github_data['data'].get('updated_at', ''),
        "public_repos": github_data['data'].get('public_repos', 0),
        "total_private_repos": github_data['data'].get('total_private_repos', 0),
        "two_factor_requirement_enabled": github_data['data'].get('two_factor_requirement_enabled', False),
        "members_allowed_repository_creation_type": github_data['data'].get('members_allowed_repository_creation_type', ''),
        "members_can_fork_private_repositories": github_data['data'].get('members_can_create_private_repositories', False),
        "web_commit_signoff_required": github_data['data'].get('web_commit_signoff_required', False),
        "is_verified": github_data['data'].get('is_verified', False),
        "plan_name": github_data['data'].get('plan', {}).get('name', ''),
        "filled_seats": github_data['data'].get('plan', {}).get('filled_seats', 0),
        "plan_private_repos": github_data['data'].get('plan', {}).get('private_repos', 0),
        "members_count": len(members_data),
        "repos_count": len(repos_data),
        "default_repository_permission": github_data['data'].get('default_repository_permission', ''),
        "has_organization_projects": github_data['data'].get('has_organization_projects', False),
        "has_repository_projects": github_data['data'].get('has_repository_projects', False),
    }

    return filtered_data
