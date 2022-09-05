from django.urls import path

from .views import (add_del_favorite,
                    add_product_in_shopping_cart,
                    reduce_product_in_shopping_cart,
                    delete_product_in_shopping_cart,
                    increase_product_in_shopping_cart,
                    category, index, product,
                    search_product)


app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('search_product', search_product, name='search_product'),
    path('category/<slug:slug>/', category, name='category'),
    path('product/<int:product_id>/', product, name='product'),
    path('product/<int:product_id>/add_del_favorite/',
         add_del_favorite,
         name='add_del_favorite'),
    path('product/<int:product_id>/add_product_in_shopping_cart/',
         add_product_in_shopping_cart,
         name='add_product_in_shopping_cart'),
    path('product/<int:product_id>/increase_product_in_shopping_cart/',
         increase_product_in_shopping_cart,
         name='increase_product_in_shopping_cart'),
    path('product/<int:product_id>/reduce_product_in_shopping_cart/',
         reduce_product_in_shopping_cart,
         name='reduce_product_in_shopping_cart'),
    path('product/<int:product_id>/delete_product_in_shopping_cart/',
         delete_product_in_shopping_cart,
         name='delete_product_in_shopping_cart'),
]
