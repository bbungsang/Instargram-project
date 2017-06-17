from django.shortcuts import render, redirect
from django.http import HttpResponse

from member.forms.login import LoginForm

from django.contrib.auth import login as django_login, logout as django_logout


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