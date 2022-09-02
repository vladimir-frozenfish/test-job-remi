from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe

from PIL import Image

from .validators import (validate_category_image_size,
                         validate_product_image_size,
                         validate_above_zero)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    favorite_product = models.ManyToManyField('Product',
                                              through='FavoriteProduct',
                                              related_name='favorite_product')
    shopping_cart = models.ManyToManyField(
        'Product',
        through='ShoppingCartProduct',
        related_name='shopping_cart'
    )

    def get_favorite_product(self):
        return ', '.join(
            self.favorite_product.all().values_list('name', flat=True)
        )

    get_favorite_product.short_description = 'Избранные товары'

    def get_shopping_cart(self):
        products = ShoppingCartProduct.objects.filter(user=self.id)
        return ", ".join((map(str, products)))

    get_shopping_cart.short_description = 'Товары в корзине'

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
        ordering = ["id"]

    def __str__(self):
        return self.username


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
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name='products',
                              verbose_name='Бренд товара')
    description = models.TextField(verbose_name='Описание товара')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория товара')
    price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                verbose_name='Стоимость товара')
    image_preview = models.ImageField(
        upload_to='product/',
        validators=[validate_product_image_size, ],
        verbose_name='Изображение предпросмотр товара',
        help_text=mark_safe(f'<span style="color:red; font-size:14px;">'
                            f'Разрешение изображения должно быть: '
                            f'{settings.PRODUCT_PREVIEW_IMAGE_RESOLUTION[0]}*{settings.PRODUCT_PREVIEW_IMAGE_RESOLUTION[1]}'
                            f'</span>')
    )

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['name']

    def __str__(self):
        return f'{self.category} {self.name}'


class FavoriteProduct(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='favorite')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Избранные товары'
        verbose_name = 'Избранный товар'
        ordering = ['user']

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_favorite_product'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.product}'


class ImageProduct(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок изображения')
    image = models.ImageField(
        upload_to='product/',
        verbose_name='Изображение товара',
        help_text=mark_safe(f'<span style="color:red; font-size:14px;">'
                            f'Если разрешение изображения слишком большое, оно будет уменьшено до '
                            f'{settings.PRODUCT_IMAGE_RESOLUTION[0]} пикселей по большей стороне'
                            f'</span>')
    )
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='images',
                                verbose_name='Изображение товара')

    def save(self, *args, **kwargs):
        """изменение размера изображения при сохранении записи"""
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > settings.PRODUCT_IMAGE_RESOLUTION[0] or img.height > settings.PRODUCT_IMAGE_RESOLUTION[1]:
            img.thumbnail(settings.PRODUCT_IMAGE_RESOLUTION)
            img.save(self.image.path)

    class Meta:
        verbose_name_plural = 'Изображения товаров'
        verbose_name = 'Изображение товаров'
        ordering = ['product']

    def __str__(self):
        return self.title


class ShoppingCartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[validate_above_zero],
        verbose_name='Количество товаров'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Товары в корзине'
        verbose_name = 'Товар в корзине'
        ordering = ['user']

        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_product_user'
            )
        ]

    def __str__(self):
        return (f'{self.product} - '
                f'{self.amount} шт.')
