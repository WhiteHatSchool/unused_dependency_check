from Project import Project


class PythonProject(Project):
    def __init__(self, hl_name: str, base_dir: str = 'repository'):
        super().__init__('Python', hl_name, base_dir)

    def _check_dependency_file(self):
        pass

    def _linting(self):
        pass