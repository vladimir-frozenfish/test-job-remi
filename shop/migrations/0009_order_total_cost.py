# Generated by Django 4.1 on 2022-09-02 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_order_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=12, verbose_name='Общая стоимость товара'),
            preserve_default=False,
        ),
    ]
