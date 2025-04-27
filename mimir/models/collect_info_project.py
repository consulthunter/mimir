
import os
import aiofiles
import aiofiles.os
from pathlib import Path

class CollectInfoProject:
    def __init__(self, project, configuration, clone, analyze, extract, export):
        self.project = project
        self.configuration = configuration
        self.clone = clone
        self.analyze = analyze
        self.extract = extract
        self.export = export

    async def run_collect(self):
        await self.clone.run_clone_async()
        await self.find_project_files(os.path.join(os.getcwd(), self.project.project_temp_dir))
        await self.analyze.run_analyze_async()
        await self.extract.run_extract()
        await self.export.run_export_async()

    async def find_project_files(self, root_dir: str):
        """
        Asynchronously find files in a given directory.
        This function will recursively walk through directories and find files.
        """
        files = []

        # Walk the directory asynchronously
        async for path in self.async_walk(root_dir):
            files.append(path)  # Collect the found files

        # Wait for all file processing tasks to complete
        self.project.project_files = files

    async def async_walk(self, root_dir: str):
        """
        Asynchronously walk through the directory tree to find files.
        """
        # This is a recursive async walk that will allow us to visit directories asynchronously.
        # We'll use aiofiles to open directories asynchronously.
        to_visit = [root_dir]  # Initial directories to visit

        while to_visit:
            dir_path = to_visit.pop()  # Get a directory to process
            try:
                # Open the directory asynchronously
                it = await aiofiles.os.scandir(dir_path)
                # Yield file paths asynchronously
                for entry in it:
                    if entry.is_file():  # If it's a file, check its extension
                        # Check if the file's extension matches any in the language's extension list
                        if any(entry.name.endswith(ext) for ext in
                               [ext for language in self.configuration.languages for ext in language["extensions"]]):
                            yield Path(dir_path) / entry.name  # Yield the file path
                    elif entry.is_dir():  # If it's a directory, add it to the list to visit
                        to_visit.append(entry.path)
            except FileNotFoundError:
                self.project.logger.log_error(f"Directory {dir_path} not found.")
            except PermissionError:
                self.project.logger.log_error(f"Permission denied: {dir_path}")