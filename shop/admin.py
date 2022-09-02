from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import (Brand,
                     Category,
                     ImageProduct,
                     FavoriteProduct,
                     Order,
                     OrderProduct,
                     Product,
                     User,
                     ShoppingCartProduct)


class CustomUserModel(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'get_shopping_cart',
        'get_favorite_product',
    )
    search_fields = ('username', 'email')
    list_display_links = ('id', 'username', 'email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent_category', 'child_category', 'image', 'get_image')
    readonly_fields = ('get_image',)
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name__iregex',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="60">')

    get_image.short_description = 'Изображение категории'

    def child_category(self, obj):
        return ', '.join(obj.child_category.all().values_list('name', flat=True))

    child_category.short_description = 'Дочерняя категория'


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name__iregex',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand',
                    'price', 'description',
                    'category', 'count_favorite',
                    'image_preview', 'get_image_preview')
    readonly_fields = ('get_image_preview',)
    list_display_links = ('id', 'name')
    search_fields = ('name__iregex',)
    list_filter = ('brand', 'category')

    def get_image_preview(self, obj):
        return mark_safe(f'<img src={obj.image_preview.url} width="100" height="100">')

    get_image_preview.short_description = 'Изображение предпросмотр товара'

    def count_favorite(self, obj):
        return FavoriteProduct.objects.filter(product=obj).count()

    count_favorite.short_description = 'Количество добавлений в избранное'


class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user',)


class ImageProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'image')
    list_filter = ('product',)


class ShoppingCartProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount')
    list_filter = ('user',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_cost', 'get_order_products', 'status', 'is_paid', 'date_ordered', 'date_sent', 'date_completed', 'shipping_method', 'city', 'address', 'comment')
    readonly_fields = ('date_ordered', 'get_order_products')
    list_filter = ('user',)
    list_display_links = ('id', 'user')


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'amount')
    list_filter = ('order',)


admin.site.register(User, CustomUserModel)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)
admin.site.register(ImageProduct, ImageProductAdmin)
admin.site.register(ShoppingCartProduct, ShoppingCartProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)

admin.site.site_title = 'Администрирование Интернет-магазина'
admin.site.site_header = 'Администрирование Интернет-магазина'




