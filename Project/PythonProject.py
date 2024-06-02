import subprocess

from Project.Project import Project


class PythonProject(Project):
    def __init__(self, hl_name: str, base_dir: str = 'repository'):
        super().__init__('Python', hl_name, base_dir)

    def _check_dependency_file(self, ver):
        ver = self.sbom_version()
        output_file_name_with_path = f'sbom/{ver}-{self.hl_name.replace("/", " ").replace(" ", "_")}.json'

        try:
            r = subprocess.run(
                args=f"cdxgen -o {output_file_name_with_path} -t python {self._local_dir_base}",
                executable='/bin/bash',
                shell=True
            )

            if r.returncode != 0:
                print(r.__dict__)
                raise "SBOM is BOOOOM!"

        except FileNotFoundError as e:
            print(f"Command not found: {e.filename}")
        except Exception as e:
            print(e)

        if ver == "old":
            self.before_sbom_path = output_file_name_with_path
        else:
            self.after_sbom_path = output_file_name_with_path

    def _linting(self):

        try:
            subprocess.run(
                args="pip-compile",
                cwd=self._local_dir_base,
                check=True,
                shell=True
            )
            
    

