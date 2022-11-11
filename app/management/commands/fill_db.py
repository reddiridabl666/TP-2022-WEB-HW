from django.core.management.base import BaseCommand
from app.models import *
import django.contrib.auth.models as auth
from faker import Faker

Faker.seed(0)

fake = Faker()


class Command(BaseCommand):
    help = "Fill db's tables, use 'ratio=<int>' to choose number of items added"

    def add_arguments(self, parser):
        pass

    @staticmethod
    def fill_users(ratio):
        users = [
            auth.User.objects.create_user(username=fake.user_name(), password=fake.password())
            for _ in range(ratio)
        ]

        for user in users:
            user.save()

    def handle(self, *args, **options):
        if len(args) > 0 or len(options) > 1:
            raise ValueError('This script accepts only keyword argument "ratio=<int>"')
        ratio = options.get('ratio', 10)

        self.fill_users(ratio)

# TAGS = [
#     "SQL", "Python", "Django",
#     "C++", "CSS", "Bootstrap",
#     "Golang"
# ]
#
# USERS = [
#     {
#         "id": user_id,
#         "name": f"User {user_id + 1}",
#         "rating": randint(0, 10),
#         "avatar": user_id if user_id < 3 else None
#     } for user_id in range(5)
# ]
#
# QUESTIONS = [
#     {
#         "id": question_id,
#         "user_id": USERS[question_id % len(USERS)]["id"],
#         "title": f"Question {question_id}",
#         "text": f"Text of question {question_id}",
#         "answer_num": 0,
#         "rating": randint(-2, 15),
#         "tag_list": sorted(sample(TAGS, 3))
#     } for question_id in range(120)
# ]
#
#
# def get_question_ids(size):
#     for answer_id in range(size):
#         yield QUESTIONS[(answer_id + randint(0, len(QUESTIONS))) % len(QUESTIONS)]['id']
#
#
# ANSWERS = [
#     {
#         "id": answer_id,
#         "user_id": USERS[answer_id % len(USERS)]["id"],
#         "question_id": question_id,
#         "text": f"Text of answer {answer_id} for question {question_id}",
#         "rating": randint(-2, 7),
#     } for answer_id, question_id in zip(range(len(QUESTIONS) * 8), get_question_ids(len(QUESTIONS) * 8))
# ]
#
# for question in QUESTIONS:
#     question['answer_num'] = len(list(filter(lambda ans: ans['question_id'] == question['id'], ANSWERS)))
