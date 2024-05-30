import os
import shutil
from abc import abstractmethod, ABC
from typing import Union

from utils.git.git_utils import clone_repo


class Project(ABC):
    _language: str
    _local_dir_base: str
    hl_name: str
    before_sbom_path: Union[str, None] = None
    after_sbom_path: Union[str, None] = None
    is_sbom_change: bool = True

    def __init__(self, language: str, hl_name: str, base_dir: str = 'repository'):
        self._language = language
        self.hl_name = hl_name
        self._local_dir_base = f'{base_dir}/{language}/{hl_name}'

        clone_repo(hl_name, self._local_dir_base)
        self._check_dependency_file(self.sbom_version())

    def __delete__(self, instance):
        shutil.rmtree(self._local_dir_base)

        if not self.is_sbom_change:
            os.remove(self.before_sbom_path)
            os.remove(self.after_sbom_path)

    @abstractmethod
    def _check_dependency_file(self, version: str):
        """
        cdxgen 이용 SBOM 을 통해 의존성을 체크
        언어마다 사전 명령어가 필요한 경우가 있으므로 반드시 하위 클래스에서 구현되도록 강제
        :return: 
        """
        pass

    @abstractmethod
    def _linting(self):
        """
        린터를 이용하여 SBOM을 통해 불필요한 의존성 제거
        언어마다 사용할 수 있는 린터가 다르므로 반드시 하위 클래스에서 구현되도록 강제
        :return:
        """
        pass

    def sbom_version(self):
        if not self.before_sbom_path:
            return 'new'
        return 'old'

    def print_dependency(self):
        if self.after_sbom_path is not None:
            os.system(f'cat {self.after_sbom_path}')
        os.system(f'cat {self.before_sbom_path}')

    def comparison_sbom(self) -> bool:
        pass

    def create_github_issue(self):
        pass

    def submit_dependency_track(self):
        pass

    def build_test(self):
        pass

