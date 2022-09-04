from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from shop.models import (ImageProduct,
                         FavoriteProduct,
                         Product,
                         User,
                         ShoppingCartProduct)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = (
                'email',
                'id',
                'username',
                'first_name',
                'last_name',
                'password'
            )
        model = User

    def create(self, validated_data):
        """создание хэшируемого пароля"""
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugField('name')
    images = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'brand',
            'category',
            'price',
            'description',
            'image_preview',
            'images',
            'is_favorited',
            'is_in_shopping_cart'
        )
        model = Product

    def get_images(self, obj):
        images = ImageProduct.objects.filter(product=obj.id)
        return [image.image.url for image in images]

    def get_is_favorited(self, obj):
        """возвращает в поле is_vaforite True если текущий пользователь
        отметил товар в избранное"""
        request_user = self.context['request'].user
        if request_user.is_anonymous:
            return False
        return FavoriteProduct.objects.filter(
            user=request_user,
            product=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """возвращает в поле is_in_shopping_cart False если текущий пользователь не
        поместил товар в корзину или количество помещенных единиц данного товара"""
        request_user = self.context['request'].user

        if request_user.is_anonymous or not ShoppingCartProduct.objects.filter(user=request_user, product=obj).exists():
            return False
        return ShoppingCartProduct.objects.get(user=request_user, product=obj).amount