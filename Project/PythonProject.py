import subprocess

from Project.Project import Project


class PythonProject(Project):
    def __init__(self, hl_name: str, base_dir: str = 'repository', sbom_base_path: str = 'sbom'):
        super().__init__('Python', hl_name, base_dir, sbom_base_path)

    def _check_dependency_file(self, sbom_path):
        try:
            r = subprocess.run(
                args=f"cdxgen -o {sbom_path} -t python {self._local_dir_base}",
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

        if self.before_sbom_path is None:
            self.before_sbom_path = sbom_path
        else:
            self.after_sbom_path = sbom_path

    def _linting(self):
        try:
            subprocess.run(
                args="pip-compile",
                cwd=self._local_dir_base,
                check=True,
                shell=True
            )
        except FileNotFoundError as e:
            print(f"Command not found: {e.filename}")
        except Exception as e:
            print(e)