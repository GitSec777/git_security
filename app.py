from flask import Flask, request
from auth.auth import auth_bp
from github_data.github_data import create_github_data_blueprint
from orgs.organization import org_bp
from repos.repository import repo_bp
from routes.org_routes import org_routes
from routes.repo_routes import repo_routes
from flask_cors import CORS
from flask_caching import Cache
import os
from services.getSecret import secret_key

app = Flask(__name__)
app.secret_key = secret_key

# Simple CORS configuration since we're using axios
CORS(app, 
     origins=["http://127.0.0.1:3000", "http://127.0.0.1:5050"],
     supports_credentials=True,
     expose_headers=["Set-Cookie"])



# Initialize cache with the main app
cache = Cache(app)

# Pass the cache object when creating the blueprint
github_data_bp = create_github_data_blueprint(cache)

# Session configuration
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False,
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

if __name__ == '__main__':
    app.run(debug=True)
