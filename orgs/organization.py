import os
from flask import Blueprint, request, jsonify, app
from utils.http_helper import send_http_request
from services.getReq import get_repo_members, get_repo_no_mfa_members, get_repo_admin_members, get_repos


org_bp = Blueprint('org', __name__)

git_token = os.getenv('GITHUB_TOKEN')

# Define routes for your API
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


def filter_org_data(org_data):
    print("org_data:",org_data)
    
    filtered_data = {
    "login": org_data.get("login"),
    "url": org_data.get("url"),
    "html_url": org_data.get("html_url"),
    "created_at": org_data.get("created_at"),
    "updated_at": org_data.get("updated_at"),
    "public_repos": org_data.get("public_repos"),
    "owned_private_repos": org_data.get("owned_private_repos"),
    "total_private_repos": org_data.get("total_private_repos"),
    "two_factor_requirement_enabled": org_data.get("two_factor_requirement_enabled"),
    "members_allowed_repository_creation_type": org_data.get("members_allowed_repository_creation_type"),
    "members_can_fork_private_repositories": org_data.get("members_can_fork_private_repositories"),
    "web_commit_signoff_required": org_data.get("web_commit_signoff_required"),
    "is_verified": org_data.get("is_verified"),
    "plan_name": org_data.get("plan", {}).get("name"),
    "filled_seats": org_data.get("plan", {}).get("filled_seats"),
    "plan_private_repos": org_data.get("plan", {}).get("private_repos"),
    "members_url": org_data.get("members_url"),
    "repos_url": org_data.get("repos_url")
    }
    return filtered_data
