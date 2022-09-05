from django.urls import include, path
from rest_framework import routers

from .views import (ProductViewSet,
                    ProductFavoriteViewSet,
                    ProductShoppingCartViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('products', ProductViewSet, basename='products')
router.register(r'products/(?P<product_id>\d+)/favorite',
                ProductFavoriteViewSet,
                basename='favorite')
router.register(r'products/(?P<product_id>\d+)/shopping_cart',
                ProductShoppingCartViewSet,
                basename='shopping_cart')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
