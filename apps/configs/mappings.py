class SystemMapping:
    api_endpoints: str = "https://mgpta-api-922713694655.asia-northeast1.run.app"

class QuestionMapping:
    summarize : str = "以下の英文を読んで，その内容を**英語で要約**し，解答欄に記入しなさい。"
    composition : str = "以下の TOPIC について，あなたの意見とその理**由を2つ**書きなさい。\n- POINTS は理由を書く際の参考となる観点を示したものです。ただし，これら以外の観点から理由を書いてもかまいません。"
    e_mail : str = "あなたは，外国人の知り合い（ {additional} ）から，Ｅメールで質問を受け取りました。この質問にわかりやすく答える返信メールを英文で書きなさい。"
    number_of_words : str = "語数の目安は{min_words}語～{max_words}語です。"
    Warning_summarize : str = "解答が英文の要約になっていないと判断された場合は，**0点と採点されることがあります。** 英文をよく読んでから答えてください。"
    Warning_composition : str = "解答が TOPIC に示された問いの答えになっていない場合や，TOPIC からずれて いると判断された場合は，**0点と採点されることがあります。** TOPIC の内容をよく 読んでから答えてください"
    Warning_e_mail : str = "解答が質問に対する返信になっていない場合や，質問に対する答えが不十分だと判断された場合は，**0点と採点されることがあります。** 質問の内容をよく読んでから答えてください。\n-  の下の Best wishes, の後にあなたの名前を書く必要はありません。"
    e_mail_addition : str = "あなたが書く返信メールの中で，{additional} のＥメール文中の下線部について，あなたがより理解を深めるために，下線部の特徴を問う具体的な質問を2つしなさい。"

class Mappings:
    def __init__(self):
        self.subject_map = {
            "英検": "eiken"
        }
        self.inverse_subject_map = {v: k for k, v in self.subject_map.items()}

        self.grade_map = {
            "３級": "3",
            "準２級": "pre2",
            "２級": "2",
            "準１級": "pre1",
            "１級": "1"
        }
        self.inverse_grade_map = {v: k for k, v in self.grade_map.items()}

        self.question_type_map = {
            "英作文": "composition",
            "英文要約": "summarize",
            "Ｅメール": "e_mail"
        }
        self.inverse_question_type_map = {v: k for k, v in self.question_type_map.items()}

        self.user_type_map = {
            "Teacher": "T",
            "Student": "S"
        }
        self.inverse_user_type_map = {v: k for k, v in self.user_type_map.items()}

    def get_mappings(self) -> dict:
        return {
            "subject_map": self.subject_map,
            "grade_map": self.grade_map,
            "question_type_map": self.question_type_map,
            "user_type_map": self.user_type_map
    }

    def get_inverse_mappings(self) -> dict:
        return {
            "inverse_subject_map": self.inverse_subject_map,
            "inverse_grade_map": self.inverse_grade_map,
            "inverse_question_type_map": self.inverse_question_type_map,
            "inverse_user_type_map": self.inverse_user_type_map
        }