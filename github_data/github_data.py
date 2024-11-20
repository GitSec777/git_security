# github_data.py

from flask import Blueprint, request, session, jsonify
import requests
from orgs.organization import get_filtered_org_data
from repos.repository import get_repo_report

def create_github_data_blueprint(cache):
    github_data_bp = Blueprint('github_data', __name__)

    # Helper function to get the GitHub token from the session and create headers
    def get_github_headers():
        token = session.get('github_token')
        if not token:
            return None
        return {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    # Route to fetch user repositories and organizations
    @github_data_bp.route('/github_data/get_user_data', methods=['GET'])
    def get_user_data_route():
        headers = get_github_headers()
        if headers is None: 
            return jsonify({'error': 'GitHub token is missing or expired.'}), 401
        print("headers are:", headers)
        # Fetch repositories
        repo_response = requests.get('https://api.github.com/user/repos', headers=headers)
        if repo_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch repositories.'}), repo_response.status_code
        repo_reports = repo_response.json()

        # Fetch organizations
        org_response = requests.get('https://api.github.com/user/orgs', headers=headers)
        if org_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch organizations.'}), org_response.status_code
        org_reports = org_response.json()

        return jsonify({
            'repos': repo_reports,
            'orgs': org_reports
        })

    # Cache the GitHub data report for 10 minutes
    @github_data_bp.route('/api/github/data', methods=['GET'])
    @cache.cached(timeout=600, key_prefix="github_report")
    def get_filtered_github_data_route():
        print("get_github_data called")
        access_token = session.get('github_token')
        org_name = request.args.get('org_name')
        repo_name = request.args.get('repo_name')

        if not access_token:
            return jsonify({'error': 'GitHub token missing or expired'}), 401

        if org_name:
            filtered_data = get_filtered_org_data(org_name, access_token)
            if 'error' in filtered_data:
                return jsonify({'error': filtered_data['error']}), 400
            print("org filtered_data:", filtered_data)
        elif repo_name:
            filtered_data = get_repo_report(repo_name, access_token)
            if 'error' in filtered_data:
                return jsonify({'error': filtered_data['error']}), 400
            print("repo filtered_data:", filtered_data)
        else:
            return jsonify({'error': 'Missing org_name or repo_name'}), 400

        return jsonify(filtered_data), 200

    return github_data_bp
