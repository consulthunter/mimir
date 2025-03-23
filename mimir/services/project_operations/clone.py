import asyncio
import os
import git
from mimir.models.project_model import ProjectModel

class Clone:
    def __init__(self, project: ProjectModel, max_retries: int = 3, timeout: int = 300):
        """
        Initialize the Clone class.

        :param project: Project details (repo URL).
        :param max_retries: Maximum number of retries for cloning.
        :param timeout: Timeout for each clone attempt in seconds.
        """
        self.project = project
        self.max_retries = max_retries
        self.timeout = timeout

    async def run_clone_async(self):
        """
        Asynchronously clone the Git repository.

        Retries cloning on failure.
        """
        attempts = 0
        while attempts < self.max_retries:
            try:
                # Start the cloning process asynchronously in a separate thread
                return await asyncio.to_thread(self.clone_repo)
            except Exception as e:
                attempts += 1
                self.project.logger.log_error(f"Attempt {attempts} failed: {e}")
                if attempts < self.max_retries:
                    self.project.logger.log_info("Retrying...")
                    await asyncio.sleep(2)  # Small delay before retry
                else:
                    self.project.logger.log_error("Max retries reached. Cloning failed.")
                    raise e

    def clone_repo(self):
        """
        Perform the Git clone operation. This is a blocking call, wrapped in `to_thread`.
        """
        repo_url = self.project.project_url
        destination_folder = self.project.project_temp_dir

        # Check if the repository already exists
        if os.path.exists(os.path.join(destination_folder, ".git")):
            self.project.logger.log_info(f"Repository already exists in {destination_folder}.")
            return

        # Ensure the destination folder is created
        os.makedirs(destination_folder, exist_ok=True)

        self.project.logger.log_info(f"Cloning repository {repo_url} into {destination_folder}...")
        try:
            # Perform the clone operation
            git.Repo.clone_from(repo_url, destination_folder)
            self.project.logger.log_info(f"Cloning completed successfully into {destination_folder}.")
        except Exception as e:
            self.project.logger.log_error(f"Failed to clone repository {repo_url}: {e}")
            raise Exception(f"Failed to clone repository: {e}")