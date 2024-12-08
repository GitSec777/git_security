# github_data.py

from flask import Blueprint, request, session, jsonify
import requests
from orgs.organization import get_filtered_org_data
from repos.repository import get_repo_report

# Create blueprint with a descriptive name
github_data_bp = Blueprint('github_data', __name__)

def get_github_headers(token):
    """
    Helper function to create GitHub API headers
    Args:
        token (str): GitHub access token
    Returns:
        dict: Headers for GitHub API requests
    """
    return {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

@github_data_bp.route('/api/github/user/data', methods=['GET'])
def get_user_data():
    """
    Get authenticated user's repositories and organizations
    Returns:
        JSON: User's GitHub data or error message
    """
    # Check authentication
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    token = session['github_token']
    headers = get_github_headers(token)

    try:
        # Fetch repositories and organizations in parallel
        repo_response = requests.get('https://api.github.com/user/repos', headers=headers)
        org_response = requests.get('https://api.github.com/user/orgs', headers=headers)

        # Check for successful responses
        if repo_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch repositories'}), repo_response.status_code
        if org_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch organizations'}), org_response.status_code

        return jsonify({
            'repos': repo_response.json(),
            'orgs': org_response.json()
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'GitHub API request failed: {str(e)}'}), 500

@github_data_bp.route('/api/github/data', methods=['GET'])
def get_filtered_data():
    """
    Get filtered data for an organization or repository
    Query Parameters:
        org_name (str): Name of the organization
        repo_name (str): Name of the repository
    Returns:
        JSON: Filtered GitHub data or error message
    """
    # Check authentication
    if 'github_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    token = session['github_token']
    org_name = request.args.get('org_name')
    repo_name = request.args.get('repo_name')

    # Validate required parameters
    if not (org_name or repo_name):
        return jsonify({'error': 'Missing org_name or repo_name parameter'}), 400

    try:
        # Get data based on provided parameters
        if org_name:
            filtered_data = get_filtered_org_data(org_name, token)
        else:
            filtered_data = get_repo_report(repo_name, token)

        # Check for errors in the filtered data
        if isinstance(filtered_data, dict) and 'error' in filtered_data:
            return jsonify({'error': filtered_data['error']}), 400

        return jsonify(filtered_data)

    except Exception as e:
        return jsonify({'error': f'Failed to fetch data: {str(e)}'}), 500

def create_github_data_blueprint(cache):
    """
    Factory function to create the blueprint with cache configuration
    Args:
        cache: Flask-Cache instance
    Returns:
        Blueprint: Configured GitHub data blueprint
    """
    if cache:
        # Apply cache decorator to the routes if cache is provided
        get_filtered_data.cached = cache.cached(timeout=600, key_prefix="github_data")
    
    return github_data_bp
