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
        print("Formatted time:", formatted_time)
        i = 1
        for commit in Repository(self.project.project_temp_dir).traverse_commits():
            print(i)
            i = i + 1
            modified_files = commit.modified_files
            for modified_file in modified_files:
                for filename in self.project.data.keys():
                    name = os.path.basename(filename)
                    if modified_file.filename.lower() == name.lower():
                        cm = CommitModel()
                        cm.commit_hash = commit.hash
                        cm.commit_author = commit.author.name
                        cm.commit_author_email = commit.author.email
                        cm.commit_message = commit.msg
                        try:
                            self.project.data[filename]["commits"].append(cm.to_dict())
                        except Exception as e:
                            pass

                        print(filename)
                        break
