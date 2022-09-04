from rest_framework import filters, viewsets, permissions, status, mixins

from shop.models import Product

from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = ProductSerializer