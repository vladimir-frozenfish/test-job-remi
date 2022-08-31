from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

from .validators import validate_category_image_size, validate_product_image_size


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to='category/',
        validators=[validate_category_image_size, ],
        verbose_name='Изображение категории',
        help_text=mark_safe(f'<span style="color:red; font-size:14px;">'
                            f'Разрешение изображения должно быть: '
                            f'{settings.CATEGORY_IMAGE_RESOLUTION[0]}*{settings.CATEGORY_IMAGE_RESOLUTION[1]}'
                            f'</span>')
    )
    parent_category = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='child_category')

    class Meta:
        verbose_name_plural = 'Категории товаров'
        verbose_name = 'Категория товара'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Бренд')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Бренды товаров'
        verbose_name = 'Бренд товара'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name='Бренд товара')
    description = models.TextField(verbose_name='Описание товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Стоимость товара')
    image_preview = models.ImageField(
        upload_to='product/',
        validators=[validate_product_image_size, ],
        verbose_name='Изображение предпросмотр товара',
        help_text=mark_safe(f'<span style="color:red; font-size:14px;">'
                            f'Разрешение изображения должно быть: '
                            f'{settings.PRODUCT_IMAGE_RESOLUTION[0]}*{settings.PRODUCT_IMAGE_RESOLUTION[1]}'
                            f'</span>')
    )

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['name']

    def __str__(self):
        return f'{self.category} {self.name}'


