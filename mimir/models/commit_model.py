
class CommitModel:
    def __init__(self):
        self.commit_hash = ""
        self.commit_date = ""
        self.commit_author = ""
        self.commit_author_email = ""
        self.commit_message = ""


    def to_dict(self):
        return {
            "commit_hash": self.commit_hash,
            "commit_date": self.commit_date,
            "commit_author": self.commit_author,
            "commit_author_email": self.commit_author_email,
            "commit_message": self.commit_message,
        }