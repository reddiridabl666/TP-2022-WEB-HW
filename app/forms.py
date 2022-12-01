import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from app.models import *

class LoginForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data
        user = authenticate(username=cleaned_data['login'], password=cleaned_data['password'])
        if user is None:
            raise forms.ValidationError('Invalid login or password')
        cleaned_data['user'] = user
        return cleaned_data


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=20)
    email = forms.EmailField()
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def save(self):
        cleaned_data = self.cleaned_data
        new_user = User.objects.create_user(cleaned_data['login'],
                                            cleaned_data['email'],
                                            cleaned_data['password'])
        UserProfile.objects.create(user=new_user, nickname=cleaned_data['nickname'])

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__exact=email).exists():
            raise forms.ValidationError('Email already taken')
        return email

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username__exact=login).exists():
            raise forms.ValidationError('Login already taken')
        return login

    def clean_repeat_password(self):
        repeat_pwd = self.cleaned_data['repeat_password']
        if self.cleaned_data['password'] != repeat_pwd:
            raise forms.ValidationError('Passwords should match')
        return repeat_pwd

    def clean_nickname(self):
        nick = self.cleaned_data['nickname']
        if UserProfile.objects.filter(nickname__exact=nick).exists():
            raise forms.ValidationError('Nickname already taken')
        return nick


class AnswerForm(forms.ModelForm):
    def save(self, user, question, commit=True):
        answer = super().save(commit=False)
        answer.profile = user.userprofile
        answer.question = question
        answer.save()
        return answer

    class Meta:
        model = Answer
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': "Enter your answer"})
        }

class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=120,
            widget=forms.TextInput(attrs={'placeholder': 'Input up to 3 tags seperated by commas'}))

    def save(self, user, commit=True):
        question = super(AskForm, self).save(commit=False)
        question.profile = user.userprofile
        question.save()

        tag_names = self.cleaned_data['tags']
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)

        question.save()
        return question

    class Meta:
        model = Question
        fields = ["title", "body", "tags"]

        labels = {
            'body': 'Text'
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Input your question's title"}),
            'body': forms.Textarea(attrs={'cols': 30, 'rows': 10, 'placeholder': "Input your question's content"})
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if re.fullmatch('(\w+(, *|$)){1,3}', tags) is None:
            if re.search('[^(\w| |,)]', tags) is not None:
                raise forms.ValidationError('You can only use letters, numbers, commas and spaces')
            raise forms.ValidationError('Make sure that you input up to 3 tags, seperated by commas')
        tags = re.split(',\s*', tags)
        return tags
