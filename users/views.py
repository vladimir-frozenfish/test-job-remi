from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('shop:index')
    template_name = 'users/signup.html'


@login_required
def cabinet(request):
    context = {}
    template = 'users/cabinet.html'

    return render(request, template, context)


@login_required
def favorite_product(request):
    products = request.user.favorite_product.all()

    context = {'products': products,}
    template = 'users/favorite_product.html'

    return render(request, template, context)
