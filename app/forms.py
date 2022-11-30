from django import forms
from django.contrib.auth.models import User
from app.models import *

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=20)
    email = forms.EmailField()
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def save(self):
        cleaned_data = self.cleaned_data
        # print(cleaned_data)
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
