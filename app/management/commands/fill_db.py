from datetime import time

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from app.models import *
import django.contrib.auth.models as auth

from faker import Faker
import faker

Faker.seed(time())

fake = Faker()


class Command(BaseCommand):
    help = "Fill db's tables, use 'ratio=<int>' to choose number of items added"

    def add_arguments(self, parser):
        parser.add_argument('--ratio',
                            help='Set ratio for filling the db. DB will be filled with {ratio} users, {ratio} * 10 questions, '
                                 '{ratio} * 100 answers, {ratio} tags, {ratio} * 200 ratings')

    def fill_users(self, ratio):
        id = auth.User.objects.all().count()

        users = [
            auth.User(username=fake.user_name() + str(id + i), password=fake.password())
            for i in range(ratio)
        ]

        auth.User.objects.bulk_create(users)

        profiles = self.fill_profiles(users)
        self.fill_questions(profiles)

    @staticmethod
    def fill_profiles(users):
        profiles = [
            UserProfile(user_id=user, avatar=str(fake.random_int(min=0, max=2)) + ".png")
            for user in users
        ]

        UserProfile.objects.bulk_create(profiles)

        return profiles

    @staticmethod
    def fill_tags(ratio):
        id = Tag.objects.all().count()

        tags = [Tag(name=fake.word() + str(id + i)) for i in range(ratio)]

        # for tag in tags:
        #     tag.save()
        Tag.objects.bulk_create(tags)

    @staticmethod
    def fill_questions(profiles):
        questions = []
        for i in range(10):
            questions.extend([Question(profile_id=profile,
                                       title=fake.sentence()[:-1] + '?',
                                       body=fake.text())
                              for profile in profiles])

        Question.objects.bulk_create(questions)


    @staticmethod
    def fill_answers():
        pass

    @staticmethod
    def fill_ratings(ratio):
        pass

    def handle(self, *args, **options):
        DEFAULT_RATIO = 10

        if len(args) > 1:
            print('This script accepts only keyword argument "ratio=<int>"')
            return

        ratio = options.get('ratio', DEFAULT_RATIO)

        print(f'Ratio is {ratio}')

        try:
            ratio = int(ratio)
        except ValueError:
            ratio = DEFAULT_RATIO

        # auth.User.objects.exclude(is_staff=True).delete()
        self.fill_users(ratio)
        self.fill_tags(ratio)
        # self.link_tags_with_questions()
        # self.fill_answers()
        # self.fill_ratings(ratio)


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
