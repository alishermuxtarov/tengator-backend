from datetime import datetime
from django.db import models


class AggregatorManager(models.Manager):
    def aggregate(self, data):
        pass

    def bid_exists(self, bid_id):
        return self.model.objects.filter(bid_id=bid_id).exists()

    def bid_create(self, **kwargs):
        kwargs['bid_date'] = datetime.strptime(
            kwargs['bid_date'], '%d.%m.%Y %H:%M:%S')
        kwargs['start_price'] = kwargs['start_price'][:-3].replace(' ', '')
        return self.model.objects.create(**kwargs)
