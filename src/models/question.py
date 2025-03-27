import json

class Question:
    def __init__(self, id, stem, answer, explanation, options):
        self.id = id
        self.question = stem
        self.answer = answer
        self.explanation = explanation if explanation else "暂无解析"
        self.options = {opt["option"]: opt["content"] for opt in options}

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            stem=data["stem"],
            answer=data["answer"],
            explanation=data["explanation"],
            options=data["options"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "explanation": self.explanation,
            "options": self.options
        }

class QuestionBank:
    def __init__(self):
        self.questions = []
        self.load_questions()

    def load_questions(self):
        with open('questions.json', 'r', encoding='utf-8') as f:
            raw_questions = json.load(f)
            self.questions = [Question.from_dict(q) for q in raw_questions]

    def get_random_questions(self, count):
        return random.sample(self.questions, min(count, len(self.questions)))

    def get_question_by_id(self, question_id):
        return next((q for q in self.questions if q.id == question_id), None)

    def get_questions_by_ids(self, question_ids):
        return [q for q in self.questions if q.id in question_ids] 