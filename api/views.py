from rest_framework import filters, viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import Product

from .serializers import ProductSerializer
from .filters import ProductFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ('name', 'category__name')
