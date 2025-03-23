import asyncio
from mimir.models.project_model import ProjectModel
from mimir.models.collect_info_project import CollectInfoProject
from mimir.services.project_operations.analyze import Analyze
from mimir.services.project_operations.clone import Clone
from mimir.services.project_operations.export import Export


class CollectInfoRunner:
    def __init__(self, configuration, logger):
        self.tasks = []
        self.configuration = configuration
        self.logger = logger
        self.projects = []
        self.get_projects()
        self.set_tasks()

    def get_projects(self):
        with open(self.configuration.target, 'r') as target:
            for line in target:
                project = ProjectModel(line, configuration=self.configuration, logger=self.logger)
                self.projects.append(project)

    def set_tasks(self):
        for project in self.projects:
            self.logger.log_info(f"Project number: {self.projects.index(project)}")
            self.logger.log_info(f"Target project {project.project_id}")
            project.ensure_project_output_dir()
            self.logger.log_info(f"Creating collect-info project {project.project_id}.")
            clone = Clone(project)
            analyze = Analyze(project)
            export = Export(project)
            collect_info = CollectInfoProject(
                project,
                self.configuration,
                clone,
                analyze,
                export,
            )
            self.tasks.append(self.run_collect_info(collect_info))

    async def run_mimir_runner(self):
        # Create batches of tasks to avoid overloading the system
        batch_size = (
            self.configuration.max_concurrency * 10
        )  # Adjust the batch size based on system capacity
        for i in range(0, len(self.tasks), batch_size):
            batch = self.tasks[i : i + batch_size]
            await asyncio.gather(*batch)

    async def run_collect_info(self, collect_info):
        semaphore = asyncio.Semaphore(self.configuration.max_concurrency)
        async with semaphore:
            try:
                self.logger.log_info(f"Running collect-info for project {collect_info.project.project_id}")
                await asyncio.gather(
                    *[collect_info.run_collect()]
                )
            except Exception as e:
                self.logger.log_error(
                    f"Error running collect-info for project {collect_info.project.project_id}: {e}"
                )