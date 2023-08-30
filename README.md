# Github Tweaks

A collection of useful scripts for Github organization admins.

## GitHub Contributors

This script aims to calculate unique contributors of GitHub organization by working with GitHub API. Also It shows contributors who commited only to 1 repository. This can be helpful when your organization is about to purchase SaaS with licence model based on number of contributors.

Last but not least the script tries to exclude contributors from previous version control services. They can appear after migration from Gitlab to GitHub or from GitHub On-Premise to GitHub Cloud.

### Usage

<code>--org_name</code> name of your organization

<code>--gh_token</code> GitHub API token. Read more how to acquire a token [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

### Usage example

```bash
$ python contributors.py --org_name test_org --gh_token <YOUR_API_TOKEN_HERE>
Organization test_org has 5 total contributors
Calculating contributors per repository...
Repository test_repo1 has 3 total contributors and 0 unique contributors: []
Repository test_repo2 has 5 total contributors and 2 unique contributors: ['user1', 'user2']
```
## Rule insights

This script collects useful statistic about [repository rulesets of Github organization](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/managing-rulesets-for-repositories-in-your-organization). It calculates specified ruleset passed rate per repository and shows the user who break the rule most times. This can be useful for ruleset evaluation since built-in ruleset insights lacks such information.

### Usage

<code>--org_name</code> name of your organization

<code>--session_cookie</code> As of August 2023 there is no API for ruleset insights. Thus it is not possible to use Github API token and value of <code>user_session</code> cookie is required

<code>--ruleset</code> name of ruleset to get statistics for

<code>--period</code> time period to gather statistic for. Default is <code>month</code>, options for <code>hour</code>,<code>day</code> and <code>week</code> are also available

### Usage example

```bash
$ python rule_insights.py --org_name test_org --session_cookie <YOUR_user_session_COOKIE_HERE> --ruleset test_ruleset
Start getting rule suite results for last month...
Received a total of 64 rule suite runs.
Calculating statistic for rule "test_ruleset" runs...
Statistics for repository test_repo1: 55.0% passed rate. Most failed actor: user1
Statistics for repository test_repo2: 100.0% passed rate. Most failed actor: no failed actors found
```