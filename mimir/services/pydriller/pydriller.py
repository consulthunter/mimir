import datetime
import os

from pydriller import Repository

from mimir.models.commit_model import CommitModel


class PyDriller:
    def __init__(self, project):
        self.project = project
        self.run_pydriller()

    def run_pydriller(self):
        # Get the current date and time
        current_time = datetime.datetime.now()
        # Print the current time in a custom format (e.g., Hour:Minute:Second)
        formatted_time = current_time.strftime("%H:%M:%S")
        self.project.logger.log_info(f"Formatted time:{formatted_time}")

        i = 1
        for commit in Repository(self.project.project_temp_dir).traverse_commits():
            modified_files = [item.filename.lower() for item in commit.modified_files]
            file_search = set(modified_files)
            i += 1
            for filename in self.project.data.keys():
                name = os.path.basename(filename).lower()
                if name in file_search:
                    cm = CommitModel()
                    cm.commit_hash = commit.hash
                    cm.commit_author = commit.author.name
                    cm.commit_date = f"{commit.author_date.year}-{commit.author_date.month}-{commit.author_date.day}"
                    cm.commit_author_email = commit.author.email
                    cm.commit_message = commit.msg
                    try:
                        self.project.data[filename].commits.append(cm)
                    except Exception as e:
                        pass
