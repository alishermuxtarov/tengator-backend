from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return '{} - {}'.format(self.bid_id, self.title)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'


class User(AbstractUser):
    uid = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.uid
        super().save(*args, **kwargs)
