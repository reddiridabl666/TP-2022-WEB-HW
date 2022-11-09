from app import models


def get_tag_list(request):
    def yield_tags():
        for i in range(0, len(models.TAGS), 3):
            yield models.TAGS[i:i + 3]

    return { 'tag_list': yield_tags }


def get_users(request):
    def yield_users():
        for user in models.USERS:
            yield user

    return { 'users': yield_users }
