from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


from shop.models import (ImageProduct,
                         FavoriteProduct,
                         Product,
                         User,
                         ShoppingCartProduct)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password')
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
        """возвращает в поле is_in_shopping_cart False если
        текущий пользователь не поместил товар в корзину или
        количество помещенных единиц данного товара"""
        request_user = self.context['request'].user

        if (request_user.is_anonymous
                or not ShoppingCartProduct.objects.filter(
                    user=request_user, product=obj
                ).exists()):
            return False
        return ShoppingCartProduct.objects.get(
            user=request_user, product=obj
        ).amount


class ProductFavoriteSerializer(serializers.ModelSerializer):
    """сериализатор для добавления рецепта в избранное"""
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        fields = ('user', 'product')
        model = FavoriteProduct

    def validate(self, data):
        user = self.context['request'].user
        product_id = self.context['view'].kwargs.get(['product_id'][0])
        product = get_object_or_404(Product, id=product_id)

        if (self.context['request'].method == 'POST'
                and FavoriteProduct.objects.filter(
                    user=user,
                    product=product).exists()):
            raise serializers.ValidationError(
                {'message': 'Вы уже добавили этот товар в избранное'}
            )

        return data


class ProductShoppingCarSerializer(serializers.ModelSerializer):
    """сериализатор для добавления товара в корзину"""
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        fields = ('user', 'product')
        model = ShoppingCartProduct

    def validate(self, data):
        user = self.context['request'].user
        product_id = self.context['view'].kwargs.get(['product_id'][0])
        product = get_object_or_404(Product, id=product_id)

        if (self.context['request'].method == 'POST'
                and ShoppingCartProduct.objects.filter(
                    user=user,
                    product=product).exists()):
            raise serializers.ValidationError(
                {'message': 'Вы уже добавили этот товар в корзину'}
            )

        return data
