from app import models


def get_tag_list(request):
    return {'tag_list': [
        models.TAGS[i:i + 3] for i in range(0, len(models.TAGS), 3)
    ]}


def get_users(request):
    return { 'users': models.USERS }
