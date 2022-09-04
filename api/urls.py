from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]