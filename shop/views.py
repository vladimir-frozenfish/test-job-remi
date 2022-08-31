from collections import deque

from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from .utils import get_all_child_categories, get_category_queue, get_category_tree


def index(request):
    """главная страница интернет-магазина"""
    categorys_main = Category.objects.filter(parent_category__isnull=True)

    template = 'shop/index.html'

    context = {'categorys': categorys_main}

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
        'category_tree': category_tree
    }

    return render(request, template, context)



