# Generated by Django 2.2.8 on 2019-12-12 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lot',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='lot',
            name='bid_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='Номер лота'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='conditions',
            field=models.TextField(verbose_name='Условия'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='customer_info',
            field=models.TextField(verbose_name='Информация о заказчике'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='start_price',
            field=models.FloatField(verbose_name='Стартовая стоимость'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='title',
            field=models.TextField(verbose_name='Наименование заказа'),
        ),
    ]
