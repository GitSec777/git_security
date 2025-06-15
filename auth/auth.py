# auth.py

from flask import Blueprint, request, redirect, session, jsonify, url_for
import requests
from services.getSecret import get_secrets

auth_bp = Blueprint('auth', __name__)

CLIENT_ID = get_secrets('client_id')
CLIENT_SECRET = get_secrets('app_secret')
FRONTEND_URL = 'http://localhost:3000'
FRONTEND_REDIRECT_URI = f'{FRONTEND_URL}/selection'

@auth_bp.route('/github/login', methods=['GET', 'POST'])
def github_login():
    # Initialize GitHub OAuth flow
    github_auth_url = "https://github.com/login/oauth/authorize"
    redirect_uri = url_for('auth.github_callback', _external=True)
    print(f"Generated redirect_uri: {redirect_uri}")
    scope = "repo read:org"
    
    # Directly redirect to GitHub's authorization page
    return redirect(f"{github_auth_url}?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}")

@auth_bp.route('/github/callback', methods=['GET'])
def github_callback():
    try:
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            return redirect(f"{FRONTEND_URL}/error?code={error}&message=Github+authorization+failed.+Please+try+again.")

        if not code:
            print("No code received")  # Debug print
            return redirect(f"{FRONTEND_URL}/error?code=authorization_failed&message=No+code+received")
        # Print the values we're using
        print(f"CLIENT_SECRET length: {len(CLIENT_SECRET) if CLIENT_SECRET else 'None'}")
        print(f"FRONTEND_URL: {FRONTEND_URL}")

        # Exchange code for access token
        token_url = 'https://github.com/login/oauth/access_token'
        token_data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': url_for('auth.github_callback', _external=True)
        }
        headers = {'Accept': 'application/json'}
        
        try:
            response = requests.post(token_url, data=token_data, headers=headers)
        except Exception as e:
            print(f"Error in token request: {str(e)}")  # Debug print
            redirect(f"{FRONTEND_URL}/error?code=connection_error&message=Failed+to+connect+to+GitHub")

        token_json = response.json()

        if 'error' in token_json:
            error_msg = token_json.get('error_description', token_json.get('error', 'Unknown error'))
            return redirect(f"{FRONTEND_URL}/error?code={token_json.get('error')}&message={error_msg}")
            
        access_token = token_json.get('access_token')
        print("access token", access_token)
        if not access_token:
            print("No access token received")  # Debug print
            return redirect(f"{FRONTEND_URL}?error=token_retrieval_failed")

        # Store token in session
        session.permanent = True
        session['github_token'] = access_token
        print("session:", dict(session))
        
        # Get user information
        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            print("user data:", user_data)
            session['user_name'] = user_data.get('name') or user_data.get('login')
        else:
            # Continue anyway, we at least have the token
            print("Warning: Could not fetch user information")
        return redirect(FRONTEND_REDIRECT_URI)

    except Exception as e:
        import traceback
        print(f"Error in callback: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        return redirect(f"{FRONTEND_URL}/error?code=server_error&message={str(e)}")

@auth_bp.route('/check-status', methods=['GET'])
def check_status():
    print("check status is happening now")
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
