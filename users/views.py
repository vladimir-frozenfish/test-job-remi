from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy

from shop.models import Order, OrderProduct, ShoppingCartProduct

from .forms import CreationForm, OrderForm
from .utils import sent_email_to_user_ordering, sent_email_to_manager_ordering


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

    context = {'products': products, }
    template = 'users/favorite_product.html'

    return render(request, template, context)


@login_required
def shopping_cart(request):
    products = ShoppingCartProduct.objects.filter(user=request.user)

    context = {'products': products, }
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
    total_cost_order = products.annotate(
        total_cost=(F('product__price') * F('amount'))
    ).aggregate(Sum('total_cost'))['total_cost__sum']

    template = 'users/ordering.html'

    form = OrderForm(request.POST or None)
    if form.is_valid():
        """сохранение заказа"""
        order = form.save(commit=False)
        order.user = request.user
        order.total_cost = total_cost_order
        order.save()

        """отправка на электронную почту уведомления
         пользователю и менеджеру об оформлении заказа"""
        sent_email_to_user_ordering(order, products)
        sent_email_to_manager_ordering(order, products)

        """сохранение в заказ товаров"""
        list_for_products = [OrderProduct(
            order=order, product=product.product, amount=product.amount
        ) for product in products]
        OrderProduct.objects.bulk_create(list_for_products)

        """удаление товаров из корзины"""
        products.delete()

        return redirect('users:order_detail', order.id)

    context = {'products': products,
               'total_cost_order': total_cost_order,
               'form': form}

    return render(request, template, context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    products = OrderProduct.objects.filter(order=order)

    template = 'users/order_detail.html'

    context = {'order': order,
               'products': products}

    return render(request, template, context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)

    template = 'users/order_list.html'

    context = {'orders': orders, }

    return render(request, template, context)
