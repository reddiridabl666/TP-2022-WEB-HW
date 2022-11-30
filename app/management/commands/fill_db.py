import random
import time

from django.core.management.base import BaseCommand
# from django.db.utils import IntegrityError

from app.models import *
import django.contrib.auth.models as auth

from faker import Faker
# import faker

Faker.seed(time.time())

fake = Faker()


class Command(BaseCommand):
    help = "Fill db's tables, use 'ratio=<int>' to choose number of items added"

    def add_arguments(self, parser):
        parser.add_argument('--ratio',
                            help='Set ratio for filling the db. DB will be filled with {ratio} users, '
                                 '{ratio} * 10 questions, '
                                 '{ratio} * 100 answers, {ratio} tags, {ratio} * 200 ratings')

    @staticmethod
    def fill_users(ratio):
        # user_id = auth.User.objects.all().count()
        #
        # users = [
        #     auth.User(username=fake.user_name() + str(user_id + i),
        #               password=fake.password(), email=fake.unique.email())
        #     for i in range(ratio)
        # ]
        #
        # auth.User.objects.bulk_create(users)

        users = auth.User.objects.all()
        for user in users:
            user.email = email=fake.unique.email()

        auth.User.objects.bulk_update(users, ['email'])

        return users

    @staticmethod
    def fill_profiles(users):
        profiles = [
            UserProfile(user=user,
                        avatar="avatars/" + str(fake.random_int(min=-1, max=2)) + ".png",
                        nickname=fake.unique.user_name())
            for user in users
        ]

        UserProfile.objects.bulk_create(profiles)

        return profiles

    @staticmethod
    def fill_tags(ratio):
        tag_id = Tag.objects.all().count()

        tags = [Tag(name=fake.word() + str(tag_id + i)) for i in range(ratio)]

        Tag.objects.bulk_create(tags)

        return tags

    @staticmethod
    def fill_questions(profiles):
        questions = []
        for i in range(10):
            questions.extend([Question(profile=profile,
                                       title=fake.sentence()[:-1] + '?',
                                       body=fake.text())
                              for profile in profiles])

        Question.objects.bulk_create(questions)

        return questions

    @staticmethod
    def fill_answers(questions, profiles):
        answers = []
        for question in questions:
            answer_num = random.randint(8, 15)
            question.answer_num = answer_num

            answers.extend([Answer(profile=random.choice(profiles),
                                   question=question,
                                   body=fake.text(max_nb_chars=400))
                            for _ in range(answer_num)])

        Answer.objects.bulk_create(answers)
        Question.objects.bulk_update(questions, ['answer_num'], batch_size=10000)

        return answers

    @staticmethod
    def link_tags_with_questions(tags, questions):
        random.seed(time.time())

        for question in questions:
            to_add = random.sample(tags, random.randint(1, 3))
            question.tags.add(*to_add)

    @staticmethod
    def fill_question_ratings(questions, profiles):
        values = [RatingType.LIKE, RatingType.LIKE, RatingType.LIKE,
                  RatingType.LIKE, RatingType.DISLIKE]

        ratings = []

        for question in questions:
            rated_users = random.sample(profiles, random.randint(10, 25))

            new_ratings = [QuestionRating(question=question,
                                      profile=user,
                                      value=random.choice(values))
                       for user in rated_users]

            for rating in new_ratings:
                question.rating += int(rating.value)

            ratings += new_ratings

        QuestionRating.objects.bulk_create(ratings, batch_size=100000)

        Question.objects.bulk_update(questions, ['rating'], batch_size=10000)

    @staticmethod
    def fill_answer_ratings(answers, profiles):
        values = [RatingType.LIKE, RatingType.LIKE, RatingType.LIKE,
                  RatingType.LIKE, RatingType.DISLIKE]

        ratings = []

        for answer in answers:
            rated_users = random.sample(profiles, random.randint(1, 5))

            new_ratings = [AnswerRating(answer=answer,
                                        profile=user,
                                        value=random.choice(values))
                           for user in rated_users]

            for rating in new_ratings:
                answer.rating += int(rating.value)

            ratings += new_ratings

        AnswerRating.objects.bulk_create(ratings, batch_size=100000)

        Answer.objects.bulk_update(answers, ['rating'], batch_size=10000)

    def handle(self, *args, **options):
        DEFAULT_RATIO = 100

        if len(args) > 1:
            print('This script accepts only keyword argument "ratio=<int>"')
            return

        ratio = options.get('ratio')

        if ratio and ratio.isdigit():
            ratio = int(ratio)
        else:
            ratio = DEFAULT_RATIO

        if ratio < DEFAULT_RATIO:
            ratio = DEFAULT_RATIO

        users = self.fill_users(ratio)
        # profiles = self.fill_profiles(users)
        # questions = self.fill_questions(profiles)
        # answers = self.fill_answers(questions, profiles)
        # tags = self.fill_tags(ratio)
        #
        # self.link_tags_with_questions(tags, questions)
        # self.fill_question_ratings(questions, profiles)
        # self.fill_answer_ratings(answers, profiles)
