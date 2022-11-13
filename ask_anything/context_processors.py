from app.models import *
from django.contrib.auth.models import User

def get_tag_list(request):
    return { 'tag_list': Tag.objects.popular().only('name') }


def get_users(request):
    return { 'users' : UserProfile.objects.best().only('user') }
