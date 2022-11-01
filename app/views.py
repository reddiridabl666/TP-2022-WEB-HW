from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET

from . import models

def get_avatars(questions):
    return [models.USERS[q['user_id']]['avatar'] for q in questions]


def sorted_by_rating(list):
    return sorted(list, key=lambda q: q['rating'], reverse=True)


def paginate(objects, request, on_page=10):
    p = Paginator(objects, on_page)


@require_GET
def index(request):
    questions = models.QUESTIONS

    context = { 'questions_avatars': zip(questions, get_avatars(questions)) }
    return render(request, 'index.html', context=context)


@require_GET
def hot(request):
    questions = sorted_by_rating(models.QUESTIONS)

    context = { 'questions_avatars': zip(questions, get_avatars(questions)) }
    return render(request, 'hot.html', context=context)


@require_GET
def question(request, question_id: int):
    if (question_id >= len(models.QUESTIONS)):
        raise Http404()

    question = models.QUESTIONS[question_id]
    answers = sorted_by_rating([ans for ans in models.ANSWERS if ans['question_id'] == question_id])

    context = {'question': question,
               'user': models.USERS[question['user_id']],
               'answers_avatars': zip(answers, get_avatars(answers))}

    return render(request, 'question.html', context=context)


@require_GET
def ask(request):
    return render(request, 'ask.html')


@require_GET
def login(request):
    return render(request, 'login.html')


@require_GET
def signup(request):
    return render(request, 'signup.html')


@require_GET
def settings(request):
    return render(request, 'settings.html')


@require_GET
def tag(request, tag_name):
    questions = sorted_by_rating([q for q in models.QUESTIONS if tag_name in q['tag_list']])

    print(request.GET.get('page'))

    context = {'tag_name': tag_name, 'questions_avatars': zip(questions, get_avatars(questions))}
    return render(request, 'tag.html', context=context)
