from Project.JavaProject import JavaProject
from utils.git.git_utils import get_search_repo_list

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
