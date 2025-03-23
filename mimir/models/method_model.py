
class MethodModel:
    def __init__(self):
        self.name = ""
        self.modifiers = []
        self.body = ""
        self.start_lin_no = 0
        self.start_pos = 0
        self.end_lin_no = 0
        self.end_pos = 0

    def to_dict(self):
        return {
            "name": self.name,
            "modifiers": self.modifiers,
            "body": self.body,
            "start_lin_no": self.start_lin_no,
            "start_pos": self.start_pos,
            "end_lin_no": self.end_lin_no,
            "end_pos": self.end_pos,
        }