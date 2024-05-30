from Project.PythonProject import PythonProject
from Project.JavaProject import JavaProject
from utils.git.git_utils import get_search_repo_list

import argparse

project_factory = {
    "Java": JavaProject,
    "Python": PythonProject
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input Project Type')

    # Define options
    parser.add_argument('-l', '--language', type=str, help='The Project Language')

    args = parser.parse_args()

    language = args.language

    # check language is in project_factory key
    if language not in project_factory.keys():
        print(", ".join(project_factory.keys()))
        exit(-1)

    repo_dir_base = 'repository'
    query_data = get_search_repo_list(language, page=1)

    total_page = query_data['page_count']
    results = query_data['results']

    repo_hl_name_list = [result['hl_name'] for result in results]

    project_list = []

    for hl_name in repo_hl_name_list:
        project = project_factory[language](hl_name)

