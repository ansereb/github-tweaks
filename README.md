# GitHub Contributors

This script aims to calculate unique contributors of GitHub organization. Also It shows contributors who commited only to 1 repository. This can be helpful when your organization is about to purchase SaaS with licence model based on number of contributors (for example SAST do so often).

## Usage

*--org_name* name of your organization
*--gh_token* GitHub API token. Read more how to acquire a token here[https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens]

## Usage example

```bash
$ python contributors.py --org_name test_org --gh_token <YOUR_API_TOKEN_HERE>
Organization test_org has 7 total contributors
Calculating contributors per repository...
Repository test_repo1 has 3 total contributors and 0 unique contributors: []
Repository test_repo2 has 4 total contributors and 2 unique contributors: ['user1', 'user2']
```