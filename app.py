from flask import Flask, request, jsonify, make_response
from config.logging_config import setup_logger
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


logger = setup_logger()

app = Flask(__name__)
app.secret_key = get_secrets('FLASK_SECRET_KEY')

# Define allowed origins based on environment
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Development React
    "http://localhost:5050",  # Development Flask
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
@app.before_request
def log_request():
    logger.info(f"Request received: {request.method} {request.path}")
    logger.info(f"Headers: {dict(request.headers)}")

@app.route('/api/health')
def health_check():
    logger.info("Health check endpoint called")
    try:
        response = make_response("OK")
        response.headers.add('Access-Control-Allow-Origin', '*')
        logger.info("Health check responding with OK")
        return response, 200
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
