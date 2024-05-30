from pathlib import Path


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