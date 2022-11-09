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
    page_num = request.GET.get('page', default=1)
    p = Paginator(objects, on_page)

    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    if page_num > p.num_pages:
        page_num = p.num_pages
    elif page_num < 1:
        page_num = 1

    return p.page(page_num), str(page_num), list(map(str, p.get_elided_page_range(page_num, on_each_side=2)))


@require_GET
def index(request):
    questions, cur_page, pages = paginate(models.QUESTIONS, request)

    context = {'questions_avatars': zip(questions, get_avatars(questions)),
               'pages': pages, 'cur_page': cur_page}

    return render(request, 'index.html', context=context)


@require_GET
def hot(request, page = 1):
    questions, cur_page, pages = paginate(sorted_by_rating(models.QUESTIONS), request)

    context = {'questions_avatars': zip(questions, get_avatars(questions)),
               'pages': pages, 'cur_page': cur_page}

    return render(request, 'hot.html', context=context)


@require_GET
def question(request, question_id: int, page = 1):
    if (question_id >= len(models.QUESTIONS)):
        raise Http404()

    question = models.QUESTIONS[question_id]
    answers = sorted_by_rating([ans for ans in models.ANSWERS if ans['question_id'] == question_id])

    answers, cur_page, pages = paginate(answers, request, 7)

    context = {'question': question,
               'user': models.USERS[question['user_id']],
               'answers_avatars': zip(answers, get_avatars(answers)),
               'pages': pages, 'cur_page': cur_page}

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
    questions, cur_page, pages = paginate(questions, request)

    context = {'tag_name': tag_name, 'pages': pages, 'cur_page': cur_page,
               'questions_avatars': zip(questions, get_avatars(questions))}

    return render(request, 'tag.html', context=context)
