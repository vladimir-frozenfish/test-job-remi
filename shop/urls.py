from django.urls import path

from .views import add_del_favorite, category, index, product


app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:slug>/', category, name='category'),
    path('product/<int:product_id>/', product, name='product'),
    path('product/<int:product_id>/add_del_favorite/', add_del_favorite, name='add_del_favorite'),
]
