from random import randint, seed, sample

import django.contrib.auth.models as auth
from django.db import models


class UserProfile(models.Model):
    user_id = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    signed_up_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Question(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)

    title = models.CharField(max_length=50)
    body = models.CharField(max_length=300)

    rating = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    body = models.CharField(max_length=300)
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
