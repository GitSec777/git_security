import requests

# Helper function for making HTTP requests
def send_http_request(url, method="GET", data=None, headers=None, params=None):
    try:
        response = requests.request(method, url, data=data, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    

    