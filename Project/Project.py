import json
import os
import shutil
from abc import abstractmethod, ABC
from typing import Union

from jycm.helper import dump_html_output
from jycm.jycm import YouchamaJsonDiffer
from starlette.config import Config

from utils.git.git_utils import clone_repo
from utils.git.github_utils import create_github_issue, get_github_repo

config = Config('.env')

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
        self._local_dir_base = f'./{base_dir}/{language}/{hl_name}'
        before_sbom_path = None
        after_sbom_path = None

        clone_repo(hl_name, self._local_dir_base)
        self._check_dependency_file(self.sbom_version())
        self._linting()
        self._check_dependency_file(self.sbom_version())
        test = self.comparison_sbom()
        if test is not None:
            print(test)
            with open(test, 'r') as content:
                repo = get_github_repo(config('ACCESS_TOKEN'), config('ORG_NAME'), config('REPO_NAME'))
                self.create_github_issue(repo, content)


        self.__delete__()

    def __delete__(self):
        shutil.rmtree(self._local_dir_base)

        if not self.is_sbom_change:
            os.remove(self.before_sbom_path)
            os.remove(self.after_sbom_path)

    @abstractmethod
    def _check_dependency_file(self, version: str) -> None:
        """
        cdxgen 이용 SBOM 을 통해 의존성을 체크
        언어마다 사전 명령어가 필요한 경우가 있으므로 반드시 하위 클래스에서 구현되도록 강제
        :return: 
        """
        pass

    @abstractmethod
    def _linting(self) -> None:
        """
        린터를 이용하여 SBOM을 통해 불필요한 의존성 제거
        언어마다 사용할 수 있는 린터가 다르므로 반드시 하위 클래스에서 구현되도록 강제
        :return:
        """
        pass

    def sbom_version(self) -> str:
        if self.before_sbom_path is not None:
            return 'new'
        return 'old'

    def print_dependency(self) -> None:
        if self.after_sbom_path is not None:
            os.system(f'cat {self.after_sbom_path}')
        os.system(f'cat {self.before_sbom_path}')

    def comparison_sbom(self) -> Union[str, None]:
        if self.before_sbom_path is not None and self.after_sbom_path is not None:
            with open(self.before_sbom_path) as old, open(self.after_sbom_path) as new:
                left = json.load(old)
                right = json.load(new)

                ycm = YouchamaJsonDiffer(left, right)
                diff_result: dict = ycm.get_diff()

                if len(diff_result.keys()) > 0:
                    url = dump_html_output(left, right, diff_result, f"/tmp/{self.hl_name}")
                    self.is_sbom_change = True
                    return url
                return None

    def create_github_issue(self, repo, body) -> None:
        create_github_issue(repo, title=f"[Demonstration] {self._language} Project: {self.hl_name}", body=body)
        pass

    def submit_dependency_track(self) -> None:
        pass

    def build_test(self) -> None:
        pass

