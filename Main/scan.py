import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))
from getReq import get_repo_admin_members, get_branches, get_branch_protection, get_branch_protection_rules, get_branches, get_repo_no_mfa_members, get_repo_members, get_repos
from getSecret import get_secrets

'''
I want to scan and use all the get functions from the getReq.py file in the services folder.
'''


org = 'GitSec777'
repo = 'git_security'
branch = 'draft1'
token = get_secrets("git_token")

def scan_org(org, token=token):
     
    members = get_repo_members(org, token)
    admins = get_repo_admin_members(org, token)
    for admin in admins:
        if members[admin["login"]]:
            members[admin["login"]]["admin"] = "True"

    no_mfas = get_repo_no_mfa_members(org, token)
    if no_mfas:
        for no_mfa in no_mfas:
            if members[no_mfa["login"]]:
                members[no_mfa["login"]]["no_mfa"] = "True"

    repos = get_repos(org, token)

    i = 0
    for repo in repos:
        repo_data = scan_repo(org, repo["name"], token)
        repos[i]["protection data"] = repo_data
    
    print("Scan Complete")
    return {org: {"members": members, "repos": repos}}
    


    
def scan_repo(org, repo, token):
    branches = get_branches(org, token)
    repo_data = {}
    for branch in branches:
        repo_data[branch["name"]] = {}
        branch_data = get_branch_protection(org, repo, branch["name"])
        if branch_data:
            branch_data = organize_data(branch_data)
            repo_data[branch["name"]]["protection"] = branch_data
        else:
            repo_data[branch["name"]]["protection"] = {}
    return repo_data


    #print(get_branches(org, token))
    #print(get_branch_protection(org, repo, branch, token))
    #print(get_branch_protection_rules(org, repo, branch, token))
    

''' I have this dict of data that I want to organize branch data and only what is protected and what isnt with most simplicty without the URL data only what is enabled and disabled
{'url': 'https://api.github.com/repos/GitSec777/git_security/branches/main/protection', 'required_pull_request_reviews': {'url': 'https://api.github.com/repos/GitSec777/git_security/branches/main/protection/required_pull_request_reviews', 'dismiss_stale_reviews': False, 'require_code_owner_reviews': False, 'require_last_push_approval': False, 'required_approving_review_count': 1}, 'required_signatures': {'url': 'https://api.github.com/repos/GitSec777/git_security/branches/main/protection/required_signatures', 'enabled': False}, 'enforce_admins': {'url': 'https://api.github.com/repos/GitSec777/git_security/branches/main/protection/enforce_admins', 'enabled': False}, 'required_linear_history': {'enabled': False}, 'allow_force_pushes': {'enabled': False}, 'allow_deletions': {'enabled': False}, 'block_creations': {'enabled': False}, 'required_conversation_resolution': {'enabled': False}, 'lock_branch': {'enabled': False}, 'allow_fork_syncing': {'enabled': False}}
'''
def organize_data(branch_data):
    organized_data = {}
    if branch_data:
        organized_data["required_pull_request_reviews"] = branch_data["required_pull_request_reviews"]["required_approving_review_count"]
        organized_data["required_signatures"] = branch_data["required_signatures"]["enabled"]
        organized_data["enforce_admins"] = branch_data["enforce_admins"]["enabled"]
        organized_data["required_linear_history"] = branch_data["required_linear_history"]["enabled"]
        organized_data["allow_force_pushes"] = branch_data["allow_force_pushes"]["enabled"]
        organized_data["allow_deletions"] = branch_data["allow_deletions"]["enabled"]
        organized_data["block_creations"] = branch_data["block_creations"]["enabled"]
        organized_data["required_conversation_resolution"] = branch_data["required_conversation_resolution"]["enabled"]
        organized_data["lock_branch"] = branch_data["lock_branch"]["enabled"]
        organized_data["allow_fork_syncing"] = branch_data["allow_fork_syncing"]["enabled"]
    return organized_data
    



org_data = scan_org(org, token)
# make a json file from org data on the data folder outside of the services folder
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../data/org_data.json")
with open(path, 'w') as outfile:
    json.dump(org_data, outfile)
















