from pydantic import BaseModel

class QuestionData(BaseModel):
    additional_instructions: list[str] | None = None
    exam_grade: str
    max_words: int
    min_words: int
    question: str
    question_type: str
    subject: str
    underlined: str | None = None
    question_id: str
    created_by: str
    created_at: int
    user_type: str
    data_name: str
    official: bool