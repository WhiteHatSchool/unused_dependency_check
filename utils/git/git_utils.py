# Github
import os

import requests
from git import Repo


def get_search_repo_list(language: str, page: int = 1) -> dict:
    """
    검색어를 통해 특정언어의 레포지토리 리스트를 스타순으로 내림차순으로 가져오는 함수
    :param language:
    :param page:
    :return: dict {"page_count": 페이지 수, "page": 검색한 page, "results": 검색 결과 리스트}
    """
    URL = make_search_query(q=f"language:{language}+", type='repositories', sort_by='stars', order='desc', page=page)

    request = requests.get(URL)
    json = request.json()['payload']

    page_count = json['page_count']
    page = json['page']
    results = json['results']

    return {"page_count": page_count, "page": page, "results": results}


def make_search_query(q: str,
                      type: str,
                      sort_by: str,
                      order: str,
                      page: int) -> str:
    """
    검색 URL를 만드는 함수
    :param q: 쿼리(검색어)
    :param type: 결과 타입(repositories, code, commits, issues, topics, wikis, users)
    :param sort_by: 정렬 기준(stars, forks, updated)
    :param order: 정렬 순서(asc, desc)
    :param page: 검색 page
    :return: url
    """
    return f'https://github.com/search?q={q}&type={type}&s={sort_by}&o={order}&p={page}'


def get_hl_name2git_url(hl_name: str) -> str:
    """
    hl_name을 git url로 변환하는 함수
    :param hl_name: hl_name
    :return: url
    """
    return f'https://github.com/{hl_name}'


# Git
def clone_repo(hl_name: str, path: str) -> None:
    """
    레포지토리를 클론하는 함수
    :param hl_name: hlname(예: 'facebook/react')
    :param path: 복사 할 경로
    :return: None
    """
    if os.path.exists(path):
        return
    print(f'Cloning {hl_name} >>> {path}...')

    Repo.clone_from(get_hl_name2git_url(hl_name), path)