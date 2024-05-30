import subprocess

from Project.Project import Project


class PythonProject(Project):
    def __init__(self, hl_name: str, base_dir: str = 'repository'):
        super().__init__('Python', hl_name, base_dir)

    def _check_dependency_file(self, ver):
        ver = self.sbom_version()
        output_file_name_with_path = f'\"{ver}-{self.hl_name.replace("/", " ").replace(" ", "_")}.json\"'

        r = subprocess.run(
            args=" ".join(f"cdxgen -o {output_file_name_with_path} -t python {self._local_dir_base}".split(" "))
        )

        if r.returncode != 0:
            raise "SBOM is BOOOOM!"

        if ver == "old":
            self.before_sbom_path = output_file_name_with_path
        else:
            self.after_sbom_path = output_file_name_with_path

    def _linting(self):
        pass

