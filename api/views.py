from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from shop.models import FavoriteProduct, Product, ShoppingCartProduct

from .serializers import (ProductSerializer,
                          ProductFavoriteSerializer,
                          ProductShoppingCarSerializer)
from .filters import ProductFilter


class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """Вьюсет для создания и удаления"""
    pass


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ('name', 'category__name')


class ProductFavoriteViewSet(CreateDeleteViewSet):
    """Вьюсет для добавления и удаления товара из избранного
    для текущего пользователя"""
    serializer_class = ProductFavoriteSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product)

    @action(methods=['delete'],
            permission_classes=(permissions.IsAuthenticated,),
            detail=False)
    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        queryset = FavoriteProduct.objects.filter(user=self.request.user,
                                                  product=product)
        if not queryset:
            return Response(
                {'message': 'Ошибка удаления товара из избранного, '
                            'возможно товара и не было в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductShoppingCartViewSet(CreateDeleteViewSet):
    """Вьюсет для добавления и удаления товара из корзины
    для текущего пользователя"""
    serializer_class = ProductShoppingCarSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product)

    @action(methods=['delete'],
            permission_classes=(permissions.IsAuthenticated,),
            detail=False)
    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        queryset = ShoppingCartProduct.objects.filter(user=self.request.user,
                                                      product=product)
        if not queryset:
            return Response(
                {'message': 'Ошибка удаления товара из корзины, '
                            'возможно товара и не было в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'],
            url_path='increase',
            permission_classes=(permissions.IsAuthenticated,),
            detail=False)
    def increase(self, request, product_id):
        product = get_object_or_404(
            ShoppingCartProduct, product__id=product_id, user=request.user
        )
        product.amount += 1
        product.save()

        return Response(
            {'message': 'Товар в корзине увеличился на одну единицу'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'],
            url_path='reduce',
            permission_classes=(permissions.IsAuthenticated,),
            detail=False)
    def reduce(self, request, product_id):
        product = get_object_or_404(
            ShoppingCartProduct, product__id=product_id, user=request.user
        )

        if product.amount > 1:
            product.amount -= 1
            product.save()
            return Response(
                {'message': 'Товар в корзине уменьшился на одну единицу'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'message': 'Количество товара не может быть меньше одного.'},
            status=status.HTTP_200_OK
        )
