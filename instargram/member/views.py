from django.shortcuts import render, redirect
from django.http import HttpResponse

from member.forms.login import LoginForm
from member.forms.signup import SignupForm

from django.contrib.auth import login as django_login, logout as django_logout, get_user_model

User = get_user_model()


def login(request):

    form = LoginForm(data=request.POST)

    if form.is_valid():

        user = form.cleaned_data['user']
        django_login(request, user)

        return redirect('post:post_list')

    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')

        form = LoginForm()
        context = {
            'form': form,
        }

        return render(request, 'member/login.html', context)


def logout(request):

    django_logout(request)

    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)

        if form.is_valid():
            user = form.create_user()
            django_login(request, user)
            return redirect('post:post_list')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)