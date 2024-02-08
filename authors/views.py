from django.shortcuts import render

from authors.forms import FormRegister

# Create your views here.


def register(request):
    form = FormRegister
    return render(request, 'authors/pages/register.html', {'form': form})
