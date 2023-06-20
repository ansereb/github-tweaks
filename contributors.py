import argparse
import requests
import uuid

github_api_url = "https://api.github.com/"

def github_api_request(url, extended_params=None):
    page_length = 100
    page_number = 1
    params = {'per_page': str(page_length), 'page': str(page_number)}
    if extended_params!=None:
        params.update(extended_params)

    headers = {'Accept': 'application/vnd.github+json', 'Authorization': 'Bearer '+args['gh_token'], 'X-GitHub-Api-Version': '2022-11-28'}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return []
    results = response.json()
    final_results = results
    #if response has more than one page
    while len(results)==page_length:
        page_number+=1
        params['page']=page_number
        results = requests.get(url, params=params, headers=headers).json()
        final_results.extend(results)
    return final_results

def get_repositories_names():
    url = github_api_url+'orgs/'+args['org_name']+'/repos'
    repositories = github_api_request(url)
    repo_names = []
    for repo in repositories:
        #dont count forks
        if repo['fork']==False:
            repo_names.append(repo['name'])
    return repo_names
    
def is_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def get_contributors_logins(repo_name):
    url = github_api_url+'repos/'+args['org_name']+'/'+repo_name+'/contributors'
    include_anon = 0
    params = {'anon': str(include_anon)}
    contributors = github_api_request(url, params)
    logins = []
    for contributor in contributors:
        login = contributor['login']
        #get rid of migration artifacts, may be uuid or 39 chars logins
        if not is_uuid(login) and len(login)!=39:
            logins.append(contributor['login'])
    return logins
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--org_name', help='Github organization name', required=True)
    parser.add_argument('--gh_token', help='Github API token', required=True)

    global args
    args = vars(parser.parse_args())
    
    repositories = get_repositories_names()
    contributors_per_repository = []
    unique_contributors = {}
    for repo in repositories:
        repo_contributors = get_contributors_logins(repo)
        for contributor in repo_contributors:
            unique_contributors[contributor]=unique_contributors.get(contributor, 0)+1
        #we can not check uniqueness of contributor before running over all of repositories
        contributors_per_repository.append({'repo_name': repo, 'contributors_count': len(repo_contributors), 'contributors': repo_contributors, 'unique_contributor_count': 0, 'unique_contributors':[]})
    print('Organization {} has {} total contributors'.format(args['org_name'], len(unique_contributors)))
    print('Calculating contributors per repository...')
    #now we can
    for repository in contributors_per_repository:
        for contributor in repository['contributors']:
            #contributor exist only in 1 repository
            if unique_contributors[contributor]==1:
                repository['unique_contributor_count']+=1
                repository['unique_contributors'].append(contributor)
    
    for repository in contributors_per_repository:
        print('Repository {} has {} total contributors and {} unique contributors: {}'.format(repository['repo_name'], repository['contributors_count'], repository['unique_contributor_count'], repository['unique_contributors']))
