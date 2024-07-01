from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.register_form import RegisterForm


def register_view(request):
    request.session['number'] = request.session.get('number') or 1
    request.session['number'] += 1

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, 'usuario registrado com sucesso')
            form = RegisterForm()

    else:
        form = RegisterForm()

    return render(request, 'authors/pages/register.html', {'form': form})
