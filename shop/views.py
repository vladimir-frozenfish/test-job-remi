from collections import deque

from django.shortcuts import get_object_or_404, render

from .models import Category
from .utils import get_category_queue, get_category_tree


def index(request):
    """главная страница интернет-магазина"""
    categorys_main = Category.objects.filter(parent_category__isnull=True)

    template = 'shop/index.html'

    context = {'categorys': categorys_main}

    return render(request, template, context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    child_categorys = category.child_category.all()

    template = 'shop/category.html'

    """получение списка категорий для отображения
    на HTML очереди категорий"""
    category_queue = get_category_queue(category)

    """получение дерева категорий"""
    category_queue_for_tree = deque(category_queue)
    category_tree = get_category_tree(category_queue_for_tree)

    context = {
        'category': category,
        'child_categorys': child_categorys,
        'category_queue': category_queue,
        'category_tree': category_tree
    }

    return render(request, template, context)



