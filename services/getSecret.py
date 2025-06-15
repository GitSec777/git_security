import json
import os
<<<<<<< HEAD

def get_secrets(key):
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../secrets/secret.json")
=======
import secrets

def get_secrets(key):
    if os.environ.get('FLASK_ENV') == 'production':
        return os.environ.get(key)
    
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../secrets/secret.json")
    print(f"Attempting to read secrets from: {path}")  # Debug print
>>>>>>> 6f1af5840efbe8c89d1e1d189e787505d20c3fb4
    with open(path) as secrets_file:
        secrets = json.load(secrets_file)

    return secrets[key]

<<<<<<< HEAD
=======

secret_key = os.getenv('FLASK_SECRET_KEY')
>>>>>>> 6f1af5840efbe8c89d1e1d189e787505d20c3fb4
