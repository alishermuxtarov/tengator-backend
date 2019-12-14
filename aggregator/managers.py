from datetime import datetime

from django.db.backends.mysql.features import DatabaseFeatures
from django.db.backends.mysql.validation import DatabaseValidation
from django.db import models, OperationalError
from django.conf import settings

def check(*args, **kwargs):
    return []


setattr(DatabaseFeatures, 'is_sql_auto_is_null_enabled', None)
DatabaseValidation.check = check


class FTSManager(models.Manager):
    def get_queryset(self):
        try:
            qs = super().get_queryset()
            qs = qs.using('fts')
            return qs
        except OperationalError:
            pass

    @staticmethod
    def clean_kwargs(kwargs):
        new_kwargs = kwargs.copy()
        for k, v in kwargs.items():
            if v is None:
                new_kwargs.pop(k)
        return new_kwargs

    def create_record(self, **kwargs):
        try:
            self.create(**self.clean_kwargs(kwargs))
        except OperationalError:
            pass

    def update_record(self, **kwargs):
        try:
            self.delete_record(kwargs.get('id'))
            self.create_record(**kwargs)
        except OperationalError:
            pass

    def search(self, word, pk=None):
        try:
            sql = "SELECT id FROM {} WHERE MATCH('{}')".format(
                self.model._meta.db_table, word)
            if pk is not None:
                sql += ' AND id = {}'.format(pk)
            sql += ';'
            qs = self.raw(sql, using='fts')
            return [i.pk for i in qs]
        except OperationalError:
            return []

    def delete_record(self, pk):
        from django.db import connections

        try:
            with connections['fts'].cursor() as cursor:
                sql = "DELETE FROM `{}` WHERE `id` = {}".format(
                    self.model._meta.db_table, pk)
                cursor.execute(sql)
                return cursor.fetchone()
        except OperationalError:
            pass

    def get_record_by_id(self, pk):
        from django.db import connections

        try:
            with connections['fts'].cursor() as cursor:
                sql = "SELECT id FROM `{}` WHERE `id` = {}".format(
                    self.model._meta.db_table, pk)
                cursor.execute(sql)
                return cursor.fetchone()
        except OperationalError:
            pass


class AggregatorManager(models.Manager):
    def aggregate(self, data):
        pass

    def bid_exists(self, bid_id):
        return self.model.objects.filter(bid_id=bid_id).exists()

    def bid_create(self, **kwargs):
        from aggregator.tasks import lot_post_save

        kwargs['bid_date'] = datetime.strptime(
            kwargs['bid_date'], '%d.%m.%Y %H:%M:%S')
        kwargs['start_price'] = kwargs['start_price'][:-3].replace(' ', '')
        files = kwargs.pop('files', None) or []

        obj = self.model.objects.create(**kwargs)
        for f in files:
            ff = obj.files.create()
            ff.file = f
            ff.save()

        if settings.DEBUG is True:
            lot_post_save(obj.pk)
        else:
            lot_post_save.delay(obj.pk)

        return obj
