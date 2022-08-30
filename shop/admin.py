from django.contrib import admin

from .models import Brand, Category, Product


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
    list_display = ('id', 'name', 'brand', 'description', 'category', 'image_preview')
    list_display_links = ('id', 'name')
    search_fields = ('name__iregex',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)


