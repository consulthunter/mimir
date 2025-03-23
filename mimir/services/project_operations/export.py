import json
import os.path

import aiofiles


class Export:
    def __init__(self, project):
        self.project = project

    async def run_export_async(self):
        export_data = self.project.data
        json_data = json.dumps(export_data, indent=4)
        file_path = os.path.join(self.project.project_output_dir, "data.json")
        # Ensure the directory exists, creating it if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        async with aiofiles.open(file_path, 'w') as file:
            await file.write(json_data)