from pydantic import BaseModel


class QARequest(BaseModel):
    question: str


class ExplainRequest(BaseModel):
    topic: str


class QuizRequest(BaseModel):
    topic: str


class SummaryRequest(BaseModel):
    text: str


class LearningPathRequest(BaseModel):
    topic: str