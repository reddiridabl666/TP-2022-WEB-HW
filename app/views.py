from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.contrib.auth import logout, login

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
    question = get_object_or_404(Question, id=question_id)
    answers, cur_page, pages = paginate(Answer.objects.of_question(question), request, 5)

    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(request.user, question)
                return HttpResponseRedirect(f'{request.path}?page={pages[-1] + "1"}#answer-{answer.id}')
        else:
            form = AnswerForm()

    context = {'question': question,
               'answers': answers,
               'pages': pages,
               'cur_page': cur_page,
               'form': form}

    return render(request, 'question.html', context=context)

def tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    questions, cur_page, pages = paginate(questions, request)

    context = {'tag_name': tag_name, 'pages': pages,
               'cur_page': cur_page, 'questions': questions}

    return render(request, 'tag.html', context=context)

@login_required(login_url='login')
def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(request.user)
            return HttpResponseRedirect(reverse('question',  args=[question.id]))
    else:
        form = AskForm()

    return render(request, 'ask.html', { "form": form })

def log_in(request):
    next = request.GET.get('next', reverse('index'))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(next)
    else:
        form = LoginForm()

    return render(request, 'login.html', { "form": form, "next": next })

@login_required(login_url='login')
def log_out(request):
    next = request.GET.get('next', reverse('index'))
    if next == reverse('ask'):
        next = reverse('index')
    logout(request)
    return HttpResponseRedirect(next)

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'signup.html', { "form": form })

@login_required(login_url='login')
def settings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        initial_data = model_to_dict(request.user)
        initial_data['nickname'] = request.user.userprofile.nickname
        form = SettingsForm(initial=initial_data)

    return render(request, 'settings.html', { 'form': form })
