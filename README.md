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
