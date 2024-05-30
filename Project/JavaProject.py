from Project.Project import Project

import subprocess

from utils.file import get_files


class JavaProject(Project):
    def __init__(self, hl_name: str, base_dir: str = 'repository'):
        super().__init__('Java', hl_name, base_dir)
        self._check_dependency_file()

    def _check_dependency_file(self):
        subprocess.run(args="pwd")
        r = subprocess.run(args=f"mvn clean compile -P clean-exclude-wars -P enhance -P embedded-jetty -DskipTests -f {self._local_dir_base}".split(" "))

        if r.returncode != 0:
            raise "Java Project Build Faild"

        ver = self.sbom_version()
        type = "java" if self.check_gradle() else "gradle"

        output_file_name_with_path = f'\"{ver}-{self.hl_name.replace("/", " ").replace(" ", "_")}.json\"'

        r = subprocess.run(
            args=" ".join(f"cdxgen -o {output_file_name_with_path} -t {type} {self._local_dir_base}".split(" "))
        )

        if r.returncode != 0:
            raise "SBOM is BOOOOM!"

        if ver == "old":
            self.before_sbom_path = output_file_name_with_path
        else:
            self.after_sbom_path = output_file_name_with_path

    def _linting(self):
        pass

    def check_gradle(self) -> bool:
        return len(get_files(self._local_dir_base,'**/build.gradle')) > 0
