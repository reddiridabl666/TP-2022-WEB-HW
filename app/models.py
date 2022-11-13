from random import randint, seed, sample

import django.contrib.auth.models as auth
from django.db import models


class UserProfile(models.Model):
    user_id = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id}`s profile'


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    profile_id = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)

    rating = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Question {self.id} of {self.profile_id.user_id}'


class Answer(models.Model):
    profile_id = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField()



class RatingType(models.TextChoices):
    LIKE = '1', 'Like'
    DISLIKE = '0', 'Dislike'


class QuestionRating(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    value = models.CharField(choices=RatingType.choices, max_length=1)


class AnswerRating(models.Model):
    question_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    value = models.CharField(choices=RatingType.choices, max_length=1)
