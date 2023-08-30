import argparse
import requests

class RepoStat:
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.passed = 0
        self.failed = 0
        self.failed_actors = []
    
    def add_result(self, result_string, actor):
        if result_string in ('allowed', 'evaluate_allowed'):
            self.passed += 1
        else:
            self.failed += 1
            self.failed_actors.append(actor)

    def calc_passed_rate(self):
        return round((self.passed / (self.passed + self.failed)), 2) * 100
    
    def most_failed_actor(self):
        if len(self.failed_actors) > 0:
            return max(self.failed_actors, key=self.failed_actors.count)
        else:
            return 'no failed actors found'



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--org_name', help='Github organization name', required=True)
    parser.add_argument('--session_cookie', help='Github user_session cookie', required=True)
    parser.add_argument('--ruleset', help='Ruleset to get statistics for', required=True)
    parser.add_argument('--period', help='Rule evaluation period', default='month', choices=['hour', 'day', 'week', 'month'])
    
    global args
    args = vars(parser.parse_args())
    print('Start getting rule suite results for last '+args['period']+'...')
    url = 'https://github.com/organizations/'+args['org_name']+'/settings/rules/insights'
    cookies = {'user_session': args['session_cookie']}
    page_number = 1
    params = {'ruleset': args['ruleset'],'time_period': args['period'], 'page': page_number}
    response = requests.get(url, params=params, cookies=cookies)
    if response.status_code != 200:
        print('Can\'t process the request')

    result = response.json()
    # ID will be needed in future to filter rule suite runs
    provided_ruleset_id = 0
    for ruleset in result['payload']['rulesets']:
        if ruleset['name'] == args['ruleset']:
            provided_ruleset_id = ruleset['id']
            break

    rule_suite_runs = result['payload']['ruleSuiteRuns']
    while result['payload']['hasMoreSuites'] == True:
        page_number += 1
        params['page']=page_number
        result = requests.get(url, params=params, cookies=cookies).json()
        rule_suite_runs.extend(result['payload']['ruleSuiteRuns'])
    print('Received a total of '+str(len(rule_suite_runs))+ ' rule suite runs.')
    print('Calculating statistic for rule "'+args['ruleset']+'" runs...')
    stats = []
    for suite_run in rule_suite_runs:
        repo_name = suite_run['repository']['name']
        repo_stat = None
        for stat in stats:
            if stat.repo_name == repo_name:
                repo_stat = stat
                break
        else:
            repo_stat = RepoStat(repo_name)
            stats.append(repo_stat)
        #rule suite contains multiple rule runs
        #saving only the result of provided rule and not the whole rule suite
        for rule_run in suite_run['ruleRuns']:
            if rule_run['rulesetId'] == provided_ruleset_id:
                repo_stat.add_result(rule_run['result'], suite_run['actor']['login'])
                break
    for stat in stats:
        print('Statistics for repository '+stat.repo_name+': '+ str(stat.calc_passed_rate())+'% passed rate. Most failed actor: '+stat.most_failed_actor())

