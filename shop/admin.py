from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent_category', 'child_category', 'image')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name__iregex',)

    def child_category(self, obj):
        return ', '.join(obj.child_category.all().values_list('name', flat=True))

    child_category.short_description = 'Дочерняя категория'


admin.site.register(Category, CategoryAdmin)
