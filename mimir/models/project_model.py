import os
from urllib.parse import urlparse
from mimir.services.logger.logger import Logger

class ProjectModel:
    def __init__(self, url, configuration, logger):
        self.project_url = url.strip()
        self.configuration = configuration
        self.project_repo = self._get_repo(url)
        self.project_owner = self._get_owner(url)
        self.project_id = f"{self.project_owner}_{self.project_repo}"
        self.logger = Logger(logger.log_dir, logger.day, logger.command, self.project_id)
        self.project_temp_dir = os.path.join(configuration.temp_dir, self.project_id)
        self.project_output_dir = os.path.join(configuration.output_dir, self.project_id)
        self.project_log_dir = configuration.log_dir
        self.project_files = []
        self.data = {}


    def _get_repo(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme in ['http', 'https']:
            path_parts = parsed_url.path.strip('/').split('/')
        else:
            path_parts = url.split(':')[-1].strip('/').split('/')
        if len(path_parts) >= 2:
            return path_parts[1].strip().replace('.git', '')
        return None

    def _get_owner(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme in ['http', 'https']:
            path_parts = parsed_url.path.strip('/').split('/')
        else:
            path_parts = url.split(':')[-1].strip('/').split('/')
        if len(path_parts) >= 2:
            return path_parts[0].strip()
        return None

    def ensure_project_output_dir(self):
        directory = os.path.dirname(self.project_output_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)