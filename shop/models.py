from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

from .validators import validate_category_image_size


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
        verbose_name_plural = "Категории товаров"
        verbose_name = "Категория товара"
        ordering = ["name"]

    def __str__(self):
        return self.name
