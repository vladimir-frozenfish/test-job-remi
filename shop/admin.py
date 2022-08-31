from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Brand, Category, FavoriteProduct, Product, User


class CustomUserModel(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'get_favorite_product',
    )
    search_fields = ('username', 'email')
    list_display_links = ('id', 'username', 'email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent_category', 'child_category', 'image')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name__iregex',)

    def child_category(self, obj):
        return ', '.join(obj.child_category.all().values_list('name', flat=True))

    child_category.short_description = 'Дочерняя категория'


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name__iregex',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'price', 'description', 'category', 'image_preview', 'count_favorite')
    list_display_links = ('id', 'name')
    search_fields = ('name__iregex',)

    def count_favorite(self, obj):
        return FavoriteProduct.objects.filter(product=obj).count()

    count_favorite.short_description = 'Количество добавлений в избранное'


class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user',)


admin.site.register(User, CustomUserModel)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)




