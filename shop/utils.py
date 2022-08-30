from collections import namedtuple

from .models import Category


def get_category_queue(category):
    """функция возвращает очередь категорий для
    построения очереди на HTML странице категорий"""
    categorys_queue = [category]

    while True:
        parent_category = categorys_queue[-1].parent_category
        if parent_category is None:
            break
        categorys_queue.append(parent_category)

    categorys_queue.reverse()

    return categorys_queue


"""именованный кортеж для формирования 
дерева категорий CFT - category_for_tree
object - объект категории
nested - отступ для категрий, для дерева
is_active - активная категория"""
CFT = namedtuple('CFT', ['object', 'nested', 'is_active'])


def get_category_tree(category_queue, nested=0):
    """функция возвращает дерево категорий, для
    построения дерева категорий на HTML странице"""
    category_tree = []

    current_category = category_queue.popleft()
    """получаем родственные категории текущей категории"""
    related_categories = Category.objects.filter(parent_category=current_category.parent_category)

    for related_category in related_categories:
        """добавляем родственную категорию в дерево"""
        category_tree.append(CFT(related_category, nested, ''))
        """категория совпадает, с той которая взята из очереди, то к ней применяем 
        рекурсивно эту же функцию"""
        if related_category.slug == current_category.slug:
            if category_queue:
                category_tree_temp = get_category_tree(category_queue, nested + 1)
                category_tree.extend(category_tree_temp)
            else:
                """если очередь пуста, то значит текущая категория активна
                меняем ей ключ на активный, а также добавляем в дерево категорий
                дочерние категории текущей"""

                """так как используются именованные кортежи и менять их нельзя,
                то сначала последнюю категорию забираем из дерева каталогов, 
                а потом опять добавляем, то с меткой, что категория активна"""
                category_temp = category_tree.pop()
                category_tree.append(CFT(category_temp.object, category_temp.nested, 'category_active'))

                child_categories = category_temp.object.child_category.all()
                for child_category in child_categories:
                    category_tree.append(CFT(child_category, nested + 1, ''))
    return category_tree

