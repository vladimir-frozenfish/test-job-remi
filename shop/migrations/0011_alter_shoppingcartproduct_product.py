# Generated by Django 4.1 on 2022-09-04 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_order_options_alter_order_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='shop.product'),
        ),
    ]
