from random import randint, seed, sample
from django.db import models

seed()

TAGS = [
    "SQL", "Python", "Django",
    "C++", "CSS", "Bootstrap",
    "Golang"
]

USERS = [
    {
        "id": user_id,
        "name": f"User {user_id + 1}",
        "rating": randint(0, 10),
        "avatar": user_id if user_id < 3 else None
    } for user_id in range(5)
]

QUESTIONS = [
    {
        "id": question_id,
        "user_id": USERS[question_id % len(USERS)]["id"],
        "title": f"Question {question_id}",
        "text": f"Text of question {question_id}",
        "answer_num": 0,
        "rating": randint(-2, 15),
        "tag_list": sorted(sample(TAGS, 3))
    } for question_id in range(5)
]


def get_question_ids(size):
    for answer_id in range(size):
        yield QUESTIONS[(answer_id + randint(0, len(QUESTIONS))) % len(QUESTIONS)]['id']


ANSWERS = [
    {
        "id": answer_id,
        "user_id": USERS[answer_id % len(USERS)]["id"],
        "question_id": question_id,
        "text": f"Text of answer {answer_id} for question {question_id}",
        "rating": randint(-2, 7),
    } for answer_id, question_id in zip(range(20), get_question_ids(20))
]

for question in QUESTIONS:
    question['answer_num'] = len(list(filter(lambda ans: ans['question_id'] == question['id'], ANSWERS)))
