from app.models import *
from django.contrib.auth.models import User

def get_tag_list(request):
    # def yield_tags():
    #     for i in range(0, min(15, Tag.objects.all().count()), 3):
    #         yield Tag.objects.all()[i:i+3]

    return { 'tag_list': Tag.objects.popular()[:15] }


def get_users(request):
    return { 'users': User.objects.annotate(models.Count('userprofile__answer'))
                                  .order_by('-userprofile__answer__count')[:5] }
