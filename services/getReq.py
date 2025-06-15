# getReq.py

import requests

# General HTTP request function
def send_http_request(url, method="GET", data=None, headers=None, params=None):
    try:
        response = requests.request(method, url, data=data, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

# Organization methods

def get_org_members(org, token):
    url = f"https://api.github.com/orgs/{org}/members"
    headers = {'Authorization': f'Bearer {token}'}
    response = send_http_request(url, method="GET", headers=headers)
    
    if response:
        members = {}
        for member in response:
            members[member["login"]] = {"id": member["id"]}
        return members
    return []

def get_org_no_mfa_members(org, token):
    url = f"https://api.github.com/orgs/{org}/members"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    params = {"filter": "2fa_disabled", "role": "all"}
    response = send_http_request(url, method="GET", headers=headers, params=params)
    no_mfa_members = []
    if response:
        for member in response:
            no_mfa_members.append({"login": member["login"], "id": member["id"], "no_mfa": "true"})
    return no_mfa_members

def get_repo_admin_members(org, token):
    url = f"https://api.github.com/orgs/{org}/members"
    headers = {'Authorization': f'Bearer {token}'}
    params = {"filter": "all", "role": "admin"}
    response = send_http_request(url, method="GET", headers=headers, params=params)
    if response:
        admin_members = [{"login": member["login"], "id": member["id"]} for member in response]
        return admin_members
    return []

def get_repos(org, token):
    url = f"https://api.github.com/orgs/{org}/repos"
    headers = {'Authorization': f'Bearer {token}'}
    response = send_http_request(url, method="GET", headers=headers)
    repos = []
    if response:
        for repo in response:
            repos.append({"name": repo["name"], "id": repo["id"]})
    return repos

def get_dependabot_alerts(org, repo, token):
    url = f"https://api.github.com/repos/{org}/{repo}/dependabot/alerts"
    headers = {'Authorization': f'Bearer {token}'}
    response = send_http_request(url, method="GET", headers=headers)
    if response:
        return response
    return []

def get_public_members(org, token):
    url = f"https://api.github.com/orgs/{org}/public_members"
    headers = {'Authorization': f'Bearer {token}', "Accept": "application/vnd.github+json"}
    response = send_http_request(url, method="GET", headers=headers)
    if response:
        return response
    return []

# Repository methods

def get_repo_report(repo_full_name, token):
    # repo_full_name should be in the format "owner/repo"
    url = f"https://api.github.com/repos/{repo_full_name}"
    headers = {'Authorization': f'Bearer {token}'}
    repo_data = send_http_request(url, method="GET", headers=headers)
    if not repo_data:
        return {'error': 'Failed to fetch repository data'}

    # Fetch branches
    branches_url = f"https://api.github.com/repos/{repo_full_name}/branches"
    branches_response = send_http_request(branches_url, method="GET", headers=headers)
    if not branches_response:
        return {'error': 'Failed to fetch branches data'}

    # Collect protection info for each branch
    branches_protection = {}
    for branch in branches_response:
        branch_name = branch['name']
        protection_url = branch['protection']['url'] if 'protection' in branch else None
        if protection_url:
            protection_data = send_http_request(protection_url, method="GET", headers=headers)
            branches_protection[branch_name] = protection_data
        else:
            branches_protection[branch_name] = None

    # Build the report
    report = {
        "name": repo_data.get('name', ''),
        "full_name": repo_data.get('full_name', ''),
        "html_url": repo_data.get('html_url', ''),
        "description": repo_data.get('description', ''),
        "created_at": repo_data.get('created_at', ''),
        "updated_at": repo_data.get('updated_at', ''),
        "pushed_at": repo_data.get('pushed_at', ''),
        "branches": branches_protection,
        # Add other relevant security data as needed
    }

    return report

def get_filtered_org_data(org_name, token):
    org_url = f"https://api.github.com/orgs/{org_name}"
    headers = {'Authorization': f'Bearer {token}'}
    org_response = send_http_request(org_url, method="GET", headers=headers)
    if not org_response:
        return {'error': 'Failed to fetch organization data'}

    # Fetch members and repos
    members_url = f"https://api.github.com/orgs/{org_name}/members"
    repos_url = f"https://api.github.com/orgs/{org_name}/repos"

    members_response = send_http_request(members_url, method="GET", headers=headers)
    repos_response = send_http_request(repos_url, method="GET", headers=headers)

    if not members_response or not repos_response:
        return {'error': 'Failed to fetch additional organization data'}

    members_data = members_response
    repos_data = repos_response

    # Get no MFA members and admin members
    no_mfa_members = get_org_no_mfa_members(org_name, token)
    admin_members = get_repo_admin_members(org_name, token)
    
    # Create the filtered data
    filtered_data = {
        "name": org_response.get('name', ''),
        "login": org_response.get('login', ''),
        "url": org_response.get('url', ''),
        "html_url": org_response.get('html_url', ''),
        "created_at": org_response.get('created_at', ''),
        "updated_at": org_response.get('updated_at', ''),
        "public_repos": org_response.get('public_repos', 0),
        "total_private_repos": org_response.get('total_private_repos', 0),
        "two_factor_requirement_enabled": org_response.get('two_factor_requirement_enabled', False),
        "members_allowed_repository_creation_type": org_response.get('members_allowed_repository_creation_type', ''),
        "members_can_fork_private_repositories": org_response.get('members_can_fork_private_repositories', False),
        "web_commit_signoff_required": org_response.get('web_commit_signoff_required', False),
        "is_verified": org_response.get('is_verified', False),
        "plan_name": org_response.get('plan', {}).get('name', ''),
        "filled_seats": org_response.get('plan', {}).get('filled_seats', 0),
        "plan_private_repos": org_response.get('plan', {}).get('private_repos', 0),
        "members_count": len(members_data),
        "repos_count": len(repos_data),
        "default_repository_permission": org_response.get('default_repository_permission', ''),
        "has_organization_projects": org_response.get('has_organization_projects', False),
        "has_repository_projects": org_response.get('has_repository_projects', False),
        "no_mfa_members": no_mfa_members,
        "admin_members": admin_members,
    }

    return filtered_data

def get_org_dependebot_alerts(org, token):
    """Get filtered dependency alerts for the organization"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.hawkgirl-preview+json'
    }
    
    url = f"https://api.github.com/orgs/{org}/dependabot/alerts"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            alerts = response.json()
            # Filter and transform the data
            filtered_alerts = []
            for alert in alerts:
                filtered_alert = {
                    'package_name': alert['dependency']['package']['name'],
                    'ecosystem': alert['dependency']['package']['ecosystem'],
                    'severity': alert['security_vulnerability']['severity'],
                    'vulnerable_version': alert['security_vulnerability']['vulnerable_version_range'],
                    'patched_version': alert['security_vulnerability']['first_patched_version']['identifier'],
                    'summary': alert['security_advisory']['summary'],
                    'created_at': alert['created_at'],
                    'state': alert['state'],
                    'repository': alert['repository']['name']
                }
                print('filtered alert🌟', filtered_alert)
                filtered_alerts.append(filtered_alert)
            
            # Sort by severity (high to low) and then by creation date
            severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            filtered_alerts.sort(
                key=lambda x: (
                    severity_order.get(x['severity'].lower(), 4),
                    x['created_at']
                )
            )
            
            return filtered_alerts
        return None
    except requests.exceptions.RequestException:
        return None

def get_org_security_advisories(org, token):
    """Get security advisories for the organization"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"https://api.github.com/orgs/{org}/security-advisories"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None


def get_repo_code_scanning_alerts(org, repo, token):
    url = f"https://api.github.com/repos/{org}/{repo}/code-scanning/alerts"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(url, headers=headers)
        if response is None:
            return {"error": "no_response"}
            
        print('code scanning response🌟', response.status_code)
        
        if response.status_code in [404, 400]:
            return {"error": "not_configured"}
        elif response.status_code == 200:
            print('code scanning response🌟', response.json())
            return response.json()
        return {"error": f"status_code_{response.status_code}"}
        
    except requests.exceptions.RequestException as e:
        print("Error in code scanning:", str(e))
        return {"error": "request_failed"}

def get_repo_secret_scanning_alerts(org, repo, token):
    url = f"https://api.github.com/repos/{org}/{repo}/secret-scanning/alerts"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(url, headers=headers)
        print('org', org, 'repo', repo, 'secret scanning response🌟', response.json())
        if response.status_code == 404:
            return {"error": "not_configured"}
        elif response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None
    
def get_repo_vul_alerts(org, repo, token):
    url = f"https://api.github.com/repos/{org}/{repo}/vulnerability-alerts"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }    
    try:
        response = requests.get(url, headers=headers)
        if response is None:
            return {"error": "no_response"}
            
        print('vulnerability response status:', response.status_code)
        
        if response.status_code == 404:
            return {"error": "not_configured"}
        elif response.status_code == 204:
            return {"status": "enabled", "message": "Vulnerability alerts are enabled"}
        
        return {"error": f"status_code_{response.status_code}"}
        
    except requests.exceptions.RequestException as e:
        print("Error in vulnerability alerts:", str(e))
        return {"error": "request_failed"}







def get_org_repo_creation_settings(org, token):
    """Get repository creation settings for the organization"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"https://api.github.com/orgs/{org}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                'members_can_create_repos': data.get('members_can_create_repositories', False),
                'members_can_create_public_repos': data.get('members_can_create_public_repositories', False),
                'members_can_create_private_repos': data.get('members_can_create_private_repositories', False),
                'members_can_create_internal_repos': data.get('members_can_create_internal_repositories', False),
                'members_allowed_repository_creation_type': data.get('members_allowed_repository_creation_type', 'none'),
                'members_can_fork_private_repos': data.get('members_can_fork_private_repositories', False),
                'default_repo_permission': data.get('default_repository_permission', 'read')
            }
        return None
    except requests.exceptions.RequestException:
        return None


