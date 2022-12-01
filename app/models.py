import django.contrib.auth.models as auth
from django.db import models

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


class UserProfileManager(models.Manager):
    def best(self):
        return self.annotate(rating=models.Sum('answer__rating')).order_by(models.F('rating').desc(nulls_last=True))


class UserProfile(models.Model):
    user = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='-1.png')
    signed_up_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=30, unique=True)

    objects = UserProfileManager()

    def __str__(self):
        return f'{self.nickname}'


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(models.Count('question')).order_by('-question__count')


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    objects = TagManager()

    def __str__(self):
        return str(self.name)


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def popular(self):
        return self.order_by('-rating')

    def by_tag(self, tag_name):
        return self.filter(tags__name__in=[tag_name]).order_by('-rating')


class Question(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)

    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)
    answer_num = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return f'Question {self.id} of {self.profile.user}'

    class Meta:
        indexes = [
            models.Index(fields=['rating'])
        ]


class AnswerManager(models.Manager):
    def of_question(self, question):
        return self.filter(question__exact=question).order_by('-rating', 'created_at')


class Answer(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    is_correct = models.BooleanField(default=False)

    rating = models.IntegerField(default=0)

    objects = AnswerManager()

    def __str__(self):
        return f'Answer {self.id} of {self.profile.user} for {self.question}'

    class Meta:
        indexes = [
            models.Index(fields=['rating'])
        ]


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

@receiver(post_save, sender=Answer)
def update_answer_count_on_save(sender, instance, created, **kwargs):
    if created:
        instance.question.answer_num += 1
        instance.question.save()

@receiver(pre_delete, sender=Answer)
def update_answer_count_on_delete(sender, instance, **kwargs):
    instance.question.answer_num -= 1
    instance.question.save()


@receiver(pre_save, sender=QuestionRating)
def update_question_rating_on_save(sender, instance, **kwargs):
    if instance.id is not None:
        instance.question.rating -= QuestionRating.objects.get(pk=instance.id).value
    instance.question.rating += int(instance.value)
    instance.question.save()


@receiver(pre_delete, sender=QuestionRating)
def update_question_rating_on_delete(sender, instance, **kwargs):
    instance.question.rating -= int(instance.value)
    instance.question.save()


@receiver(pre_save, sender=AnswerRating)
def update_answer_rating_on_save(sender, instance, **kwargs):
    if instance.id is not None:
        instance.answer.rating -= AnswerRating.objects.get(pk=instance.id).value
    instance.answer.rating += int(instance.value)
    instance.answer.save()


@receiver(pre_delete, sender=AnswerRating)
def update_answer_rating_on_delete(sender, instance, **kwargs):
    instance.answer.rating -= int(instance.value)
    instance.answer.save()
