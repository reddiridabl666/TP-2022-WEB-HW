from django.db import models

# Create your models here.
QUESTIONS = [
    {
        "id": question_id,
        "title": f"Question {question_id}",
        "text": f"Text of question {question_id}",
        "answers_num": question_id ** 2
    } for question_id in range(5)
]
