import json
import os

def get_secrets(key):
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../secrets/secret.json")
    with open(path) as secrets_file:
        secrets = json.load(secrets_file)

    return secrets[key]

