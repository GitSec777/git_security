from flask import Flask, Blueprint, request, redirect, session, jsonify
import requests
import os

auth_bp = Blueprint('auth', __name__)

CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
FRONTEND_REDIRECT_URI = 'http://localhost:3000/selection' 


@auth_bp.route('/auth/github/callback', methods=['GET', 'POST'])
def github_callback():
    print("GitHub callback route reached")  # Debugging line
    
    code = request.args.get('code')
    if not code:
        return "Authorization failed: Missing code", 400

    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': 'http://127.0.0.1:5000/auth/github/callback'
    }
    headers = {'Accept': 'application/json'}
    
    response = requests.post(token_url, data=token_data, headers=headers)
    print("GitHub Response:", response.json())  # Log the GitHub response

    token_json = response.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return "Failed to retrieve access token.", 400

    session['github_token'] = access_token
    return redirect(FRONTEND_REDIRECT_URI)

@auth_bp.route('/get_github_token', methods=['GET'])
def get_github_token():
    print("Getting GitHub token")  # Debugging line
    token = session.get('github_token')

    if token:
        return jsonify({'github_token': token})
    else:
        return jsonify({'error': 'No token found'}), 401