# Generated by Django 4.1 on 2022-08-31 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_favoriteproduct_user_favorite_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок изображения')),
                ('image', models.ImageField(upload_to='product/', verbose_name='Изображение товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product', verbose_name='Изображение товара')),
            ],
            options={
                'verbose_name': 'Изображение товаров',
                'verbose_name_plural': 'Изображения товаров',
                'ordering': ['product'],
            },
        ),
    ]
