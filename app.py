from flask import Flask, request, jsonify, make_response
from auth.auth import auth_bp
from github_data.github_data import create_github_data_blueprint
from orgs.organization import org_bp
from repos.repository import repo_bp
from routes.org_routes import org_routes
from routes.repo_routes import repo_routes
from flask_cors import CORS
from flask_caching import Cache
import os
from services.getSecret import get_secrets

app = Flask(__name__)
app.secret_key = get_secrets('FLASK_SECRET_KEY')

# Define allowed origins based on environment
ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",  # Development React
    "http://127.0.0.1:5050",  # Development Flask
]

# Add production ALB origin if in production
if os.environ.get('FLASK_ENV') == 'production':
    alb_domain = os.environ.get('ALB_DOMAIN')
    if alb_domain:
        ALLOWED_ORIGINS.extend([
            "http://git-sec-alb-1454068422.eu-west-1.elb.amazonaws.com",
            "https://git-sec-alb-1454068422.eu-west-1.elb.amazonaws.com"
        ])

# Configure CORS with the appropriate origins
CORS(app, 
     origins=ALLOWED_ORIGINS,
     supports_credentials=True,
     expose_headers=["Set-Cookie"])

# Initialize cache with the main app
cache = Cache(app)


# Pass the cache object when creating the blueprint
github_data_bp = create_github_data_blueprint(cache)

# Session configuration
# Session configuration
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=os.environ.get('FLASK_ENV') == 'production',  # True in production
    SESSION_COOKIE_HTTPONLY=True
)

# Cache configuration
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 600

# Register all blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(github_data_bp)
app.register_blueprint(org_bp)
app.register_blueprint(repo_bp)
app.register_blueprint(org_routes)
app.register_blueprint(repo_routes)


# Add health check endpoint for AWS
@app.route('/api/health')
def health_check():
    app.logger.info("Health check endpoint called")
    try:
        response = make_response("OK")
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    except Exception as e:
        app.logger.error("Health check error: %s", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
