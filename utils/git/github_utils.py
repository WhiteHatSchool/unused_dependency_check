from github import Github


def get_github_repo(access_token, org_name: str, repository_name: str):
    g = Github(access_token)
    repo = g.get_organization(org_name).get_repo(repository_name)
    return repo


def create_github_issue(repo, title, body):
    repo.create_issue(title=title, body=body)
