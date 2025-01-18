class Mappings:
    def __init__(self):
        self.subject_map = {
            "英検": "eiken"
        }

        self.level_map = {
            "３級": "3",
            "準２級": "pre2",
            "２級": "2",
            "準１級": "pre1",
            "１級": "1"
        }

        self.question_type_map = {
            "英作文": "composition",
            "英文要約": "summary",
            "Ｅメール": "email"
        }

        self.user_type_map = {
            "Teacher": "T",
            "Student": "S"
        }

    def get_mappings(self) -> dict:
        return {
            "subject_map": self.subject_map,
            "level_map": self.level_map,
            "question_type_map": self.question_type_map,
            "user_type_map": self.user_type_map
        }