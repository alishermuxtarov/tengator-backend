import binascii
import os

from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from aggregator import managers


class Region(models.Model):
    title = models.TextField('Регион')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Area(models.Model):
    region = models.ForeignKey(Region, related_name='areas', on_delete=models.CASCADE)
    title = models.TextField('Район')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Category(models.Model):
    title = models.TextField('Категория')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE)
    title = models.TextField('Список товаров')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список товаров'
        verbose_name_plural = 'Список товаров'


class Lot(models.Model):
    bid_date = models.DateTimeField('Срок окончания торгов')
    bid_id = models.PositiveIntegerField('Номер лота')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Район')
    title = models.TextField('Наименование заказа')
    start_price = models.FloatField('Стартовая стоимость')
    conditions = models.TextField('Условия')
    customer_info = models.TextField('Информация о заказчике')
    description = models.TextField('Описание')
    url = models.URLField('Источник', unique=True, max_length=150)
    category = models.ForeignKey(Category, null=True, verbose_name='Категория', on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory, blank=True, verbose_name='Список товаров')
    has_request = models.BooleanField('Наличие заявок', default=False)

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
    # todo: add TEXT Version

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


class Token(models.Model):
    key = models.CharField(max_length=40, verbose_name=_("Ключ"), unique=True)
    user = models.ForeignKey(User, models.CASCADE, related_name='tokens', verbose_name=_("Пользователь"))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name=_(u'Время создания'))

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Токен")
        verbose_name_plural = _("Токены")


class SearchWord(models.Model):
    user = models.ForeignKey(
        'aggregator.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    word = models.CharField('Поисковое слово', max_length=255)

    class Meta:
        verbose_name = "Сохраненные параметры поиска"
        verbose_name_plural = "Сохраненные параметры поиска"


class FtsTengator(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(default='')
    files = models.TextField(default='')
    description = models.TextField(default='')

    objects = managers.FTSManager()

    class Meta:
        managed = False
        db_table = 'tengator'
