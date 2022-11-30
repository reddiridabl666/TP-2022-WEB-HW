from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_GET

from app.models import *
from app.forms import *

def paginate(objects, request, on_page=10):
    page_num = request.GET.get('page', default='1')
    p = Paginator(objects, on_page)

    if page_num.isdigit():
        page_num = int(page_num)
    else:
        page_num = 1

    if page_num > p.num_pages:
        page_num = p.num_pages
    elif page_num < 1:
        page_num = 1

    return p.page(page_num), str(page_num), list(map(str, p.get_elided_page_range(page_num, on_each_side=2)))

def index(request):
    questions, cur_page, pages = paginate(Question.objects.new(), request)

    context = {'questions': questions,
               'pages': pages, 'cur_page': cur_page}

    return render(request, 'index.html', context=context)

def hot(request, page = 1):
    questions, cur_page, pages = paginate(Question.objects.popular(), request)

    context = {'questions': questions,
               'pages': pages, 'cur_page': cur_page}

    return render(request, 'hot.html', context=context)

def question(request, question_id: int, page = 1):
    try:
        question = Question.objects.get(id=question_id)
    except:
        raise Http404()

    answers, cur_page, pages = paginate(Answer.objects.of_question(question), request, 5)

    context = {'question': question,
               'answers': answers,
               'pages': pages,
               'cur_page': cur_page}

    return render(request, 'question.html', context=context)

def tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    questions, cur_page, pages = paginate(questions, request)

    context = {'tag_name': tag_name, 'pages': pages,
               'cur_page': cur_page, 'questions': questions}

    return render(request, 'tag.html', context=context)

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'signup.html', { "form": form })

def settings(request):
    return render(request, 'settings.html')
