from starlette.config import Config

from utils.git.github_utils import create_github_issue, get_github_repo

config = Config('../.env')
repo = get_github_repo(config('ACCESS_TOKEN'), config('ORG_NAME'), config('REPO_NAME'))
print(repo)

create_github_issue(repo, 'test', 'test')