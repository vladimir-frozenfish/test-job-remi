from django.urls import path

from .views import category, index, product


app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:slug>/', category, name='category'),
    path('product/<int:product_id>/', product, name='product'),
]
