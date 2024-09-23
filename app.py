from flask import Flask
from auth.auth import auth_bp
from github_data.github_data import create_github_data_blueprint
from orgs.organization import org_bp
from repos.repository import repo_bp
from flask_cors import CORS
from flask_caching import Cache
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')



# Initialize cache with the main app
cache = Cache(app)

# Pass the cache object when creating the blueprint
github_data_bp = create_github_data_blueprint(cache)


############################################################################################################
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True  # Use True if your site is served over HTTPS
)

# Cache configuration
app.config['CACHE_TYPE'] = 'simple'  # Simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 600  # Cache timeout set to 10 minutes

# Initialize cache with the main app

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(github_data_bp)
app.register_blueprint(org_bp)
app.register_blueprint(repo_bp)

if __name__ == '__main__':
    app.run(debug=True)
