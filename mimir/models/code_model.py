from typing import List

from mimir.models.class_model import ClassModel
from mimir.models.commit_model import CommitModel


class CodeModel:
    def __init__(self, language):
        self.language = language
        self.imports = []
        self.namespace = ""
        self.code_classes: List[ClassModel] = []
        self.commits : List[CommitModel] = []

    def to_dict(self):
        return {
            'language': self.language,
            "imports": self.imports,
            "namespace": self.namespace,
            'code_classes': [cla.to_dict() for cla in self.code_classes],
            'commits': [commit.to_dict() for commit in self.commits],
        }