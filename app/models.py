from random import randint, seed, sample
from django.db import models

seed()

tag_list = [
    "SQL", "Python", "Django",
    "C++", "CSS", "Bootstrap"
]

QUESTIONS = [
    {
        "id": question_id,
        "user_id": 0,
        "title": f"Question {question_id}",
        "text": f"Text of question {question_id}",
        "answer_num": 0,
        "rating": randint(-2, 15),
        "tag_list": sample(tag_list, 3)
    } for question_id in range(5)
]


def get_question_ids(size):
    for answer_id in range(size):
        yield QUESTIONS[(answer_id + randint(0, len(QUESTIONS))) % len(QUESTIONS)]['id']


ANSWERS = [
    {
        "id": answer_id,
        "user_id": 0,
        "question_id": question_id,
        "text": f"Text of answer {answer_id} for question {question_id}",
        "rating": randint(-2, 7),
    } for answer_id, question_id in zip(range(20), get_question_ids(20))
]

for question in QUESTIONS:
    question['answer_num'] = len(list(filter(lambda ans: ans['question_id'] == question['id'], ANSWERS)))
