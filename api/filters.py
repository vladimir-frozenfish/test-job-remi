from django_filters.rest_framework import CharFilter, FilterSet, filters

from shop.models import Product


class ProductFilter(FilterSet):
    category = CharFilter(
        field_name='category__slug', method='filter_category'
    )

    is_favorited = filters.BooleanFilter(
        method="filter_is_favorited"
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )

    class Meta:
        model = Product
        fields = ['category', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, value, obj):
        if obj:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value, obj):
        if obj:
            return queryset.filter(cart__user=self.request.user)
        return queryset
