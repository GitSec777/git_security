# auth.py

from flask import Blueprint, request, redirect, session, jsonify, url_for
import requests
from services.getSecret import get_secrets

auth_bp = Blueprint('auth', __name__)

CLIENT_ID = get_secrets('client_id')
CLIENT_SECRET = get_secrets('app_secret')
FRONTEND_URL = 'http://localhost:3000'
FRONTEND_REDIRECT_URI = f'{FRONTEND_URL}/selection'

@auth_bp.route('/github/login', methods=['GET'])
def github_login():
    # Initialize GitHub OAuth flow
    github_auth_url = "https://github.com/login/oauth/authorize"
    redirect_uri = url_for('auth.github_callback', _external=True)
    scope = "repo read:org"
    
    # Directly redirect to GitHub's authorization page
    return redirect(f"{github_auth_url}?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}")

@auth_bp.route('/github/callback', methods=['GET'])
def github_callback():
    code = request.args.get('code')
    if not code:
        return redirect(f"{FRONTEND_URL}?error=authorization_failed")

    # Exchange code for access token
    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': url_for('auth.github_callback', _external=True)
    }
    headers = {'Accept': 'application/json'}
    
    response = requests.post(token_url, data=token_data, headers=headers)
    
    token_json = response.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return redirect(f"{FRONTEND_URL}?error=token_retrieval_failed")

    # Store token in session
    session['github_token'] = access_token
    
    # Get user information
    user_response = requests.get(
        'https://api.github.com/user',
        headers={'Authorization': f'token {access_token}'}
    )
    
    if user_response.status_code == 200:
        user_data = user_response.json()
        session['user_name'] = user_data.get('name') or user_data.get('login')
    
    return redirect(FRONTEND_REDIRECT_URI)

@auth_bp.route('/check-status', methods=['GET'])
def check_status():
    if 'github_token' not in session:
        return jsonify({'isAuthenticated': False}), 401
    
    return jsonify({
        'isAuthenticated': True,
        'name': session.get('user_name', 'GitHub User')
    })

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})
