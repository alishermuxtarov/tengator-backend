from django.db import models
from aggregator import managers


class Lot(models.Model):
    bid_date = models.DateTimeField('Срок окончания торгов')
    bid_id = models.PositiveIntegerField('Номер лота', unique=True)
    region = models.CharField('Регион', max_length=150)
    area = models.CharField('Район', max_length=150)
    title = models.TextField('Наименование заказа')
    start_price = models.FloatField('Стартовая стоимость')
    conditions = models.TextField('Условия')
    customer_info = models.TextField('Информация о заказчике')

    objects = managers.AggregatorManager()

    class Meta:
        ordering = ['-id']
