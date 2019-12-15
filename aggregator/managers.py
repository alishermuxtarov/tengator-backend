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

    def bid_update_requests(self, bid_id, has_request):
        return self.model.objects.filter(bid_id=bid_id).update(has_request=has_request)

    def bid_create(self, sub_ref, **kwargs):
        from aggregator.tasks import lot_post_save
        from aggregator.models import SubCategory

        kwargs['bid_date'] = datetime.strptime(
            kwargs['bid_date'], '%d.%m.%Y %H:%M:%S')
        kwargs['start_price'] = kwargs['start_price'][:-3].replace(' ', '')
        files = kwargs.pop('files', None) or []
        subcategories = kwargs.pop('subcategories', [])

        obj = self.model.objects.create(**kwargs)

        for s in subcategories:
            if s not in sub_ref:
                # c, _ = Category.objects.get_or_create(title=category)
                so = SubCategory.objects.create(
                    title=s, category_id=kwargs['category_id'])
                sub_ref[so.title] = so.pk
            obj.sub_category.add(sub_ref[s])
        obj.save()

        for f in files:
            ff = obj.files.create()
            ff.file = f
            ff.save()

        if settings.DEBUG is True:
            lot_post_save(obj.pk)
        else:
            lot_post_save.delay(obj.pk)

        return obj

    def categories_report(self):
        query = """
            SELECT c.id, c.title, count(l.id) total_count, round(sum(start_price)) total_price,
                   sum((CASE WHEN start_price BETWEEN 0 AND 5000000 THEN 1 ELSE 0 END)) price0,
                   sum((CASE WHEN start_price BETWEEN 5000001 AND 10000000 THEN 1 ELSE 0 END)) price1,
                   sum((CASE WHEN start_price BETWEEN 10000001 AND 30000000 THEN 1 ELSE 0 END)) price2,
                   sum((CASE WHEN start_price BETWEEN 30000001 AND 50000000 THEN 1 ELSE 0 END)) price3,
                   sum((CASE WHEN start_price BETWEEN 50000001 AND 70000000 THEN 1 ELSE 0 END)) price4,
                   sum((CASE WHEN start_price BETWEEN 70000001 AND 100000000 THEN 1 ELSE 0 END)) price5,
                   sum((CASE WHEN start_price > 100000001 THEN 1 ELSE 0 END)) price6
            FROM aggregator_lot l
            LEFT JOIN aggregator_category c on l.category_id = c.id
            GROUP BY category_id
            ORDER BY total_price DESC;
        """
        return self.raw(query)
