from django.urls import path

from .views import index, category


app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:slug>/', category, name='category'),
]
