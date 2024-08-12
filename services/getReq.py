import requests
from getSecret import get_secrets

git_token = get_secrets("git_token")



# general http request function
def send_http_request(url, method="GET", data=None, headers=None, params=None):
    try:
        
        response = requests.request(method, url, data=data, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception if status code is not 2xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# organization methods
############################

# get all members of the organization GitSec777
def get_repo_members(org, token=git_token):
    url = f"https://api.github.com/orgs/{org}/members"
    my_headers = {'Authorization': 'Bearer ' + token }
    response = send_http_request(url, method="GET", headers=my_headers)
    
    if response:
        members = {}
        for member in response:
            members[member["login"]] = {"id":member["id"]}
        return members
    else:
        return []
    


# get all members of the organization GitSec777 that have not enabled MFA
def get_repo_no_mfa_members(org, token=git_token):
    url = f"https://api.github.com/orgs/{org}/members"
    my_headers = {'Authorization': 'Bearer ' + token }
    my_params = {"filter": "2fa_disabled"}
    response = send_http_request(url, method="GET", headers=my_headers, params=my_params )
    #print(response)
    no_mfa_members = []
    if response:
        for member in response:
            no_mfa_members.append( {"login": member["login"], "id":member["id"], "no_mfa":"true" } )  
        return no_mfa_members


#get all members of the organization GitSec777 that have admin role
def get_repo_admin_members(org, token=git_token):
    url = f"https://api.github.com/orgs/{org}/members"
    my_headers = {'Authorization': 'Bearer ' + token }
    my_params = {"filter": "all", "role": "admin"}
    response = send_http_request(url, method="GET", headers=my_headers, params=my_params)
    if response:
        #make a list of all admin members with only login and id

        admin_members = []
        for member in response:
            admin_members.append( {"login": member["login"], "id":member["id"] } )  
        return admin_members

#repository methods
#/orgs/{org}/repos

def get_repos(org, token=git_token):
    url = f"https://api.github.com/orgs/{org}/repos"
    my_headers = {'Authorization': 'Bearer ' + token }
    response = send_http_request(url, method="GET", headers=my_headers)
    repos = []
    if response:
        for repo in response:
            repos.append( {"name": repo["name"], "id": repo["id"] } )
        return repos
    else:
        return []


# branch methods
# /repos/{owner}/{repo}/branches/{branch}/protection
def get_branch_protection_rules(org, repo, branch, token=git_token):
    url = f"https://api.github.com/repos/{org}/{repo}/branches/{branch}/protection"
    my_headers = {'Authorization': 'Bearer ' + token }

    response = send_http_request(url, method="GET", headers=my_headers)
    if response:
        return response
    else:
        return []
    
    
def get_branches(org, token=git_token):
    url = f"https://api.github.com/repos/{org}/git_security/branches"
    my_headers = {'Authorization': 'Bearer ' + token }
    response = send_http_request(url, method="GET", headers=my_headers)
    branches = []
    if response:
        for branch in response:
            # we can add required status checks as well if needed.
            branches.append( {"name": branch["name"], "protected": branch["protected"] } )
        return branches
    else:
        return []       

def get_branch_protection(org, repo, branch, token=git_token):
    url = f"https://api.github.com/repos/{org}/{repo}/branches/{branch}/protection"
    my_headers = {'Authorization': 'Bearer ' + token }
    response = send_http_request(url, method="GET", headers=my_headers)
    if response:
        return response
    else:
        return []

def set_branch_protection(branch, repo_owner, repo_name, token=git_token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch}/protection"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.github.luke-cage-preview+json'
    }
    #minimum required settings for branch protection
    data = {
        "required_status_checks": {
            "strict": True,
            "contexts": []
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1
        },
        "restrictions": None
    }

    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Branch protection set successfully.")
        return response.json()
    else:
        print("Failed to set branch protection.", response.status_code, response.text)
        return None

def remove_branch_protection(branch, repo_owner, repo_name, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch}/protection"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.github.luke-cage-preview+json'
    }

    response = requests.delete(url, headers=headers)
    if response.status_code == 204:  # HTTP 204 No Content means the deletion was successful
        print("Branch protection removed successfully.")
        return True
    else:
        print(f"Failed to remove branch protection. Status Code: {response.status_code}")
        print("Response:", response.text)
        return False

# /repos/{owner}/{repo}/dependabot/alerts
def get_dependabot_alerts(org, repo, token=git_token):
    url = f"https://api.github.com/repos/{org}/{repo}/dependabot/alerts"
    my_headers = {'Authorization': 'Bearer ' + token }
    response = send_http_request(url, method="GET", headers=my_headers)
    if response:
        return response
    else:
        return []
    





# Example usage
org = 'GitSec777'
repo = 'git_security'
branch = 'main'

    


print('branch protection', get_branch_protection(org, repo, branch))

print('admin members are:', get_repo_admin_members(),'\n\n')
print('no mfa members are:', get_repo_no_mfa_members(),'\n\n')

#print('branch protection rules are:', get_branch_protection_rules())
#print('branches are:', get_branches(org))
#update_branch_protection('draft1')
#print('remove branch protection:', remove_branch_protection('draft1', 'GitSec777', 'git_security', git_token))
#print('branches are:', get_branches(org))

#print('dependebot alerts are:', get_dependabot_alerts('GitSec777', 'git_security'))


