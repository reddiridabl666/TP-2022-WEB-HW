from django.shortcuts import render
# from django.http import HttpResponse
from django.views.decorators.http import require_GET

from . import models


@require_GET
def index(request):
    context = {'question': models.QUESTIONS}
    return render(request, 'index.html', context=context)


@require_GET
def question(request, question_id: int):
    context = {'question': models.QUESTIONS[question_id]}
    return render(request, 'question.html', context=context)


@require_GET
def ask(request):
    return render(request, 'ask.html')


@require_GET
def settings(request):
    return render(request, 'settings.html')
