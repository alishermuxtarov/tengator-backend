from django.contrib.auth.models import AbstractUser
from django.db import models

from aggregator import managers


class Lot(models.Model):
    bid_date = models.DateTimeField('Срок окончания торгов')
    bid_id = models.PositiveIntegerField('Номер лота')
    region = models.CharField('Регион', max_length=150)
    area = models.CharField('Район', max_length=150)
    title = models.TextField('Наименование заказа')
    start_price = models.FloatField('Стартовая стоимость')
    conditions = models.TextField('Условия')
    customer_info = models.TextField('Информация о заказчике')
    description = models.TextField('Описание')
    url = models.URLField('Источник', unique=True)

    objects = managers.AggregatorManager()

    def __str__(self):
        return '{} - {}'.format(self.bid_id, self.title)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'


class LotFile(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'


class User(AbstractUser):
    uid = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.uid
        super().save(*args, **kwargs)


class SearchWord(models.Model):
    user = models.ForeignKey(
        'aggregator.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    word = models.CharField('Поисковое слово', max_length=255)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class FtsTengator(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(default='')
    files = models.TextField(default='')
    description = models.TextField(default='')

    objects = managers.FTSManager()

    class Meta:
        managed = False
        db_table = 'tengator'
