import django.contrib.auth.models as auth
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}`s profile'


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(models.Count('question')).order_by('-question__count')

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    objects = TagManager()

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)

    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Question {self.id} of {self.profile.user}'


class Answer(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Answer {self.id} of {self.profile.user} for {self.question}'


class RatingType(models.TextChoices):
    LIKE = (1, 'Like')
    DISLIKE = (-1, 'Dislike')


def readable_rating(num):
    if num == 1:
        return 'Like'
    else:
        return 'Dislike'

class QuestionRating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=RatingType.choices)

    def __str__(self):
        return f'{readable_rating(self.value)} by {self.profile.user} for {self.question}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'profile'],
                                    name='Users can`t add more than one rating for question')
        ]

        indexes = [
            models.Index(fields=['question', 'profile'])
        ]


class AnswerRating(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=RatingType.choices)

    def __str__(self):
        return f'{readable_rating(self.value)} by {self.profile.user} for {self.answer}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['answer', 'profile'],
                                    name='Users can`t add more than one rating for answer')
        ]

        indexes = [
            models.Index(fields=['answer', 'profile'])
        ]
