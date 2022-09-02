from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from shop.models import ShoppingCartProduct

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


@login_required
def shopping_cart(request):
    products = ShoppingCartProduct.objects.filter(user=request.user)

    context = {'products': products,}
    template = 'users/shopping_cart.html'

    return render(request, template, context)


@login_required
def clean_shopping_cart(request):
    products = ShoppingCartProduct.objects.filter(user=request.user)
    products.delete()

    return redirect('users:shopping_cart')
