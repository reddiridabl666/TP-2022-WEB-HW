from django.shortcuts import render
# from django.http import HttpResponse
from django.views.decorators.http import require_GET

from . import models


@require_GET
def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context=context)


@require_GET
def popular(request):
    context = {'questions': sorted(models.QUESTIONS, key=lambda q: q['rating'], reverse=True)}
    return render(request, 'popular.html', context=context)


@require_GET
def question(request, question_id: int):
    question_answers = [ans for ans in models.ANSWERS if ans['question_id'] == question_id]
    context = {'question': models.QUESTIONS[question_id], 'answers': question_answers}
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
    context = {'tag_name': tag_name}
    return render(request, 'tag.html', context=context)
