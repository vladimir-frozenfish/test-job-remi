from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from shop.models import OrderProduct, ShoppingCartProduct

from .forms import CreationForm, OrderForm


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


@login_required
def ordering(request):
    products = ShoppingCartProduct.objects.filter(user=request.user)

    """получение общей стоимости заказа"""
    total_cost_order = products.annotate(total_cost=(F('product__price')*F('amount'))).aggregate(Sum('total_cost'))['total_cost__sum']

    template = 'users/ordering.html'

    form = OrderForm(request.POST or None)
    if form.is_valid():
        """сохранение заказа"""
        order = form.save(commit=False)
        order.user = request.user
        order.total_cost = total_cost_order
        order.save()

        """сохранение в заказ товаров"""
        list_for_products = [OrderProduct(order=order, product=product.product, amount=product.amount) for product in products]
        OrderProduct.objects.bulk_create(list_for_products)

        """удаление товаров из корзины"""
        products.delete()

        return redirect('shop:index')

    context = {'products': products,
               'total_cost_order': total_cost_order,
               'form': form}

    return render(request, template, context)
