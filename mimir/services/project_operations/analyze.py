from mimir.parsers.java_parser import JavaParser
from mimir.services.pydriller.pydriller import PyDriller


class Analyze:
    def __init__(self, project):
        self.project = project

    async def run_analyze_async(self):
        self.project.logger.log_info(f"Analyzing for project {self.project.project_id}")
        for file in self.project.project_files:
            ext = file.suffix
            for language in self.project.configuration.languages:
                if ext in language['extensions']:
                    if language['name'] == 'java':
                        JavaParser(self.project, file)
                    break

        self.run_pydriller_analyze()

    def run_pydriller_analyze(self):
        self.project.logger.log_info(f"Running PyDriller Analysis for project {self.project.project_id}")
        PyDriller(self.project)