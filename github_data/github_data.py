from flask import Blueprint, request, session, jsonify
import requests
from orgs.organization import get_filtered_org_data
from repos.repository import get_repo_report

def create_github_data_blueprint(cache):
    github_data_bp = Blueprint('github_data', __name__)

    # Helper function to get the GitHub token from the session and create headers
    def get_github_headers():
        token = session.get('github_token')
        print('token:', token)
        if not token:
            return None
        return {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    # Route to fetch user repositories and organizations
    @github_data_bp.route('/get_user_data', methods=['GET'])
    def get_user_data():
        headers = get_github_headers()
        if headers is None: 
            return jsonify({'error': 'GitHub token is missing or expired.'}), 401

        # Fetch repositories
        repo_response = requests.get('https://api.github.com/user/repos', headers=headers)
        repo_reports = [repo for repo in repo_response.json()]

        if repo_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch repositories.'}), repo_response.status_code

        # Fetch organizations
        org_response = requests.get('https://api.github.com/user/orgs', headers=headers)
        org_reports = [org for org in org_response.json()]

        if org_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch organizations.'}), org_response.status_code

        return jsonify({
            'repos': repo_reports,
            'orgs': org_reports
        })

    # Cache the GitHub data report for 10 minutes
    @github_data_bp.route('/api/github/data', methods=['GET'])
    @cache.cached(timeout=600, key_prefix="github_report")
    def get_github_data():
        print("get_github_data called")
        access_token = session.get('github_token')
        org_name = request.args.get('org_name')
        repo_name = request.args.get('repo_name')

        if not access_token:
            return jsonify({'error': 'GitHub token missing or expired'}), 401
        
        headers = {'Authorization': f'Bearer {access_token}'}
        if org_name:
            url = f'https://api.github.com/orgs/{org_name}'
        elif repo_name:
            url = f'https://api.github.com/repos/{repo_name}'
        else:
            return jsonify({'error': 'Missing org_name or repo_name'}), 400
        
        response = requests.get(url, headers=headers)

        # Filter the data based on whether it's an organization or repository
        if org_name:
            filtered_data = filter_org_data(response.json())
            print("org filtered_data:", filtered_data)
        if repo_name:
            filtered_data = get_repo_report(response.json())
            print("repo filtered_data:", filtered_data)
        
        return jsonify(filtered_data), response.status_code

    return github_data_bp