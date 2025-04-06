from mimir.models.commit_model import CommitModel
from mimir.models.method_model import MethodModel
from typing import List


class ClassModel:
    def __init__(self):
        self.name = ""
        self.modifiers = []
        self.properties = []
        self.methods: List[MethodModel] = []
        self.start_lin_no = 0
        self.start_pos = 0
        self.end_lin_no = 0
        self.end_pos = 0

    def to_dict(self):
        return {
            "name": self.name,
            "modifiers": self.modifiers,
            "properties": self.properties,
            "methods": [method.to_dict() for method in self.methods],
            "start_lin_no": self.start_lin_no,
            "start_pos": self.start_pos,
            "end_lin_no": self.end_lin_no,
            "end_pos": self.end_pos,
        }