import json
import os
import secrets

def get_secrets(key):
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../secrets/secret.json")
    print(f"Attempting to read secrets from: {path}")  # Debug print
    with open(path) as secrets_file:
        secrets = json.load(secrets_file)

    return secrets[key]


secret_key = os.getenv('FLASK_SECRET_KEY')
