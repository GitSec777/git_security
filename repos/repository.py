import os
from flask import Blueprint, request, jsonify
from utils.http_helper import send_http_request
from services.getReq import get_repo_members, get_repo_no_mfa_members, get_repo_admin_members, get_repos, get_dependabot_alerts

repo_bp = Blueprint('repo', __name__)
git_token = os.getenv('GITHUB_TOKEN')

def get_repo_report(github_response):
    # Extract necessary fields for the report
    report = {
        "repository_name": github_response.get("full_name"),
        "visibility": github_response.get("visibility"),
        "has_issues_enabled": github_response.get("has_issues"),
        "has_projects_enabled": github_response.get("has_projects"),
        "open_issues_count": github_response.get("open_issues_count"),
        "default_branch": github_response.get("default_branch"),
        "permissions": github_response.get("permissions"),
        "allow_forking": github_response.get("allow_forking"),
        "has_wiki_enabled": github_response.get("has_wiki"),
        "allow_squash_merge": github_response.get("allow_squash_merge"),
        "allow_merge_commit": github_response.get("allow_merge_commit"),
        "web_commit_signoff_required": github_response.get("web_commit_signoff_required"),
        "delete_branch_on_merge": github_response.get("delete_branch_on_merge"),
        "forks_count": github_response.get("forks_count"),
        "subscribers_count": github_response.get("subscribers_count")
    }
    
    # Return the selected fields to the frontend
    return report


@repo_bp.route('/repo/branches', methods=['GET'])
def get_repo_branches():
    org = request.args.get('org')
    repo = request.args.get('repo')
    response = get_branches(org, git_token)
    return jsonify(response)

@repo_bp.route('/repo/branch/protection', methods=['GET'])
def get_branch_protection():
    org = request.args.get('org')
    repo = request.args.get('repo')
    branch = request.args.get('branch')
    response = get_branch_protection(org, repo, branch, git_token)
    return jsonify(response)

@repo_bp.route('/repo/branch/protection/set', methods=['POST'])
def set_branch_protection():
    data = request.json
    branch = data.get('branch')
    repo_owner = data.get('repo_owner')
    repo_name = data.get('repo_name')
    response = set_branch_protection(branch, repo_owner, repo_name, git_token)
    return jsonify(response)

@repo_bp.route('/repo/branch/protection/remove', methods=['POST'])
def remove_branch_protection():
    data = request.json
    branch = data.get('branch')
    repo_owner = data.get('repo_owner')
    repo_name = data.get('repo_name')
    response = remove_branch_protection(branch, repo_owner, repo_name, git_token)
    return jsonify({'success': response})

@repo_bp.route('/repo/dependabot/alerts', methods=['GET'])
def get_dependabot_alerts():
    org = request.args.get('org')
    repo = request.args.get('repo')
    response = get_dependabot_alerts(org, repo, git_token)
    return jsonify(response)



    