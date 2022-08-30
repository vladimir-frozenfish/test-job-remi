from PIL import Image

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_category_image_size(image):
    img = Image.open(image)
    if img.width != settings.CATEGORY_IMAGE_RESOLUTION[0] or img.height != settings.CATEGORY_IMAGE_RESOLUTION[1]:
        raise ValidationError(f'Разрешение изображения не соответствует требуемым: '
                              f'{settings.CATEGORY_IMAGE_RESOLUTION[0]}x{settings.CATEGORY_IMAGE_RESOLUTION[1]}')


def validate_product_image_size(image):
    img = Image.open(image)
    if img.width != settings.PRODUCT_IMAGE_RESOLUTION[0] or img.height != settings.PRODUCT_IMAGE_RESOLUTION[1]:
        raise ValidationError(f'Разрешение изображения не соответствует требуемым: '
                              f'{settings.PRODUCT_IMAGE_RESOLUTION[0]}x{settings.PRODUCT_IMAGE_RESOLUTION[1]}')
