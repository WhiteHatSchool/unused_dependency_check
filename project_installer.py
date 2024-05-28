import os
from abc import abstractmethod
from pathlib import Path
from typing import Union, Final
import requirements
import requests
from git import Repo

dependencies_file = {
    'JavaScript': ['**/package.json'],
    'Python': ['**/requirements.txt',],# '**/setup.py', '**/pyproject.toml'],
    'Java': ['**/pom.xml', '**/build.gradle'],
    'Go': ['**/go.mod'],
    'Ruby': ['**/Gemfile', '**/Gemfile.lock'],
    'Rust': ['**/Cargo.toml'],
    'C#': ['**/packages.config', '**/Project.csproj'],
}


class Component:
    name: str
    specs: list[tuple[str, str]]  # example :  [('>=', '1.11'), ('<', '1.12')]

    def __init__(self, name: str, specs: list[tuple[str, str]]):
        self.name = name
        self.specs = specs


class Project:
    language: Union[str, None] = None
    hl_name: str
    local_dir_base: str
    before_dependencies: list[Component] = []

    def __init__(self, language: str, hl_name: str, base_dir: str = 'repository'):
        self.language = language
        self.hl_name = hl_name
        self.local_dir_base = f'{base_dir}/{language}/{hl_name}'

        clone_repo(hl_name, self.local_dir_base)

    def __delete__(self, instance):
        os.rmdir(self.local_dir_base)

    @abstractmethod
    def check_dependency_file(self):
        if self.language is None:
            dependency_list = []
            for key in dependencies_file:
                dependency_list += [file for dependency in dependencies_file[key] for file in
                                    get_files(self.local_dir_base, dependency)]
            return dependency_list
        else:
            return [file for dependency in dependencies_file[language] for file in get_files(self.local_dir_base+'/../', dependency)]

    def print_dependency(self):
        for dependency in self.before_dependencies:
            print(dependency.name, dependency.specs)

    @abstractmethod
    def delete_dead_code(self):
        pass

    @abstractmethod
    def delete_unused_code(self):
        pass


class PythonProject(Project):
    def __init__(self, hl_name: str, base_dir: str = 'repository'):
        super().__init__('Python', hl_name, base_dir)
        self.check_dependency_file()

    def check_dependency_file(self):
        dependency_file_list = super().check_dependency_file()

        for file in dependency_file_list:
            with open(file, 'r') as f:
                for req in requirements.parse(f):
                    self.before_dependencies.append(Component(req.name, req.specs))

    def delete_dead_code(self):
        pass

    def delete_unused_code(self):
        pass


class JavaProject(Project):
    def __init__(self, hl_name: str, base_dir: str = 'repository'):
        super().__init__('Java', hl_name, base_dir)
        self.check_dependency_file()

    def check_dependency_file(self):
        dependency_file_list = super().check_dependency_file()

    def delete_dead_code(self):
        pass

    def delete_unused_code(self):
        pass



# Github
def get_search_repo_list(language: str, page: int = 1) -> dict:
    """
    검색어를 통해 특정언어의 레포지토리 리스트를 스타순으로 내림차순으로 가져오는 함수
    :param language:
    :param page:
    :return: dict {"page_count": 페이지 수, "page": 검색한 page, "results": 검색 결과 리스트}
    """
    URL = make_search_query(q=f"language:{language}", type='repositories', sort_by='stars', order='desc', page=page)

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
    if os.path.isdir(path + hl_name):
        return
    print(f'Cloning {hl_name}...')

    Repo.clone_from(get_hl_name2git_url(hl_name), path + hl_name)


def get_files(target_path: str, file_format: str) -> list:
    """
    와일드 카드를 사용하여 파일을 찾는 함수
    :param target_path: "/path/to/directory"
    :param file_format: "**/*.txt"
    :return: list of Path
    """
    path_list = []
    for path in Path(target_path).glob(file_format):
        path_list.append(str(path))

    return path_list


def get_include_dependency(target_path: str, language: Union[str, None] = None) -> list:
    """
    언어에 따른 의존성 파일을 찾는 함수(재귀적으로 찾음)
    :param target_path: "/path/to/directory"
    :param language: 언어
    :return: target_path에 있는 의존성 파일 리스트
    """
    if language is None:
        dependency_list = []
        for key in dependencies_file:
            dependency_list += [file for dependency in dependencies_file[key] for file in
                                get_files(target_path, dependency)]
        return dependency_list
    else:
        return [file for dependency in dependencies_file[language] for file in get_files(target_path, dependency)]


if __name__ == '__main__':
    language = 'Java'
    repo_dir_base = 'repository'
    query_data = get_search_repo_list(language, page=1)

    total_page = query_data['page_count']
    results = query_data['results']

    repo_hl_name_list = [result['hl_name'] for result in results]

    project_list = []

    for hl_name in repo_hl_name_list:
        project_list.append(JavaProject(hl_name))

    for project in project_list:
        project.print_dependency()
