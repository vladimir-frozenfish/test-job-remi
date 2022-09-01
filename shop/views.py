from collections import deque

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect

from .models import Category, ImageProduct, FavoriteProduct, Product
from .forms import OrderingForm
from .utils import get_all_child_categories, get_category_queue, get_category_tree


def index(request):
    """главная страница интернет-магазина"""

    """получение начальных категорий, тех у которых нет 
    родительских категорий"""
    categorys_main = Category.objects.filter(parent_category__isnull=True)

    """получение продуктов отсортированных 
    по количеству добавлений в избранное - 
    получаем 3 таких продукта"""
    products = Product.objects.all().annotate(favorite_count=Count('favorite')).order_by('-favorite_count')[:3]

    template = 'shop/index.html'

    context = {'categorys': categorys_main,
               'products': products}

    return render(request, template, context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    child_categorys = category.child_category.all()

    """получение продуктов"""
    if child_categorys:
        """если у текущей категории есть дочерние категории, 
        то сначала получаем все дочерние категории вглубину до конца от текущей,
        потом получаем все товары в этих категориях"""
        all_child_categories = get_all_child_categories(child_categorys)
        products = Product.objects.filter(category__in=all_child_categories)
    else:
        """если у текущей категории нет дочерних категорий, 
        т.е. она конечная в глубину, то получаем все товары
        текущей категории"""
        products = category.products.all()

    """сортировка товаров"""
    current_order = 'name'
    form_ordering = OrderingForm(request.GET)
    if form_ordering.is_valid():
        if form_ordering.cleaned_data.get('order'):
            current_order = form_ordering.cleaned_data.get('order')
            products = products.order_by(current_order)

    template = 'shop/category.html'

    """получение списка категорий для отображения
    на HTML очереди категорий"""
    category_queue = get_category_queue(category)

    """получение дерева категорий"""
    category_queue_for_tree = deque(category_queue)
    category_tree = get_category_tree(category_queue_for_tree)

    context = {
        'category': category,
        'products': products,
        'child_categorys': child_categorys,
        'category_queue': category_queue,
        'category_tree': category_tree,
        'form_ordering': form_ordering,
        'current_order': current_order
    }

    return render(request, template, context)


def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ImageProduct.objects.filter(product=product)

    """получение списка категорий для отображения
        на HTML очереди категорий"""
    category_queue = get_category_queue(product.category)

    """получение дерева категорий"""
    category_queue_for_tree = deque(category_queue)
    category_tree = get_category_tree(category_queue_for_tree)

    """проверка является ли текущий товар в избранном
    у аутентифицированного пользователя"""
    is_favorite_product = (
            request.user.is_authenticated
            and FavoriteProduct.objects.filter(user=request.user, product=product).exists()
    )

    template = 'shop/product.html'

    context = {
        'product': product,
        'category_queue': category_queue,
        'category_tree': category_tree,
        'images': images,
        'is_favorite_product': is_favorite_product
    }

    return render(request, template, context)


@login_required
def add_del_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    favorite_product, created = FavoriteProduct.objects.get_or_create(
        product=product, user=request.user
    )

    if not created:
        favorite_product.delete()

    return redirect('shop:product', product_id)




