import requests
from getSecret import get_secrets

git_token = get_secrets("git_token")

# general http request function
def send_http_request(url, method="GET", data=None, headers=None, params=None):
    try:
        response = requests.request(method, url, data=data, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception if status code is not 2xx
        #print(response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# get all members of the organization GitSec777 that have not enabled MFA
def get_repo_no_mfa_members():
    url = "https://api.github.com/orgs/GitSec777/members"
    my_headers = {'Authorization': git_token, "filter": "2fa_disabled" }
    response = send_http_request(url, method="GET", headers=my_headers )
    
    no_mfa_members = []
    if response:
        for member in response:
            no_mfa_members.append( {"login": member["login"], "id":member["id"], "no_mfa":"true" } )  
        return no_mfa_members


#get all members of the organization GitSec777 that have admin role
def get_repo_admin_members():
    url = "https://api.github.com/orgs/GitSec777/members"
    my_headers = {'Authorization': git_token }
    my_params = { "filter": "all", "role": "admin"}
    response = send_http_request(url, method="GET", headers=my_headers, params=my_params)
    if response:
        #make a list of all admin members with only login and id

        admin_members = []
        for member in response:
            admin_members.append( {"login": member["login"], "id":member["id"] } )  
        return admin_members
    






print('admin members are:', get_repo_admin_members(),'\n\n')
print('no mfa members are:', get_repo_no_mfa_members())

