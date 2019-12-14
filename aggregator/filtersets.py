from datetime import datetime, timedelta

from django_filters import rest_framework as filters

from aggregator.models import Lot, FtsTengator


class LotFilter(filters.FilterSet):
    q = filters.CharFilter(method='filter_q')
    hot_lots = filters.BooleanFilter(method='filter_hot_lots')
    start_price_from = filters.NumberFilter(field_name='start_price', lookup_expr='gte')
    start_price_to = filters.NumberFilter(field_name='start_price', lookup_expr='lte')
    bid_date_from = filters.NumberFilter(field_name='bid_date', lookup_expr='gte')
    bid_date_to = filters.NumberFilter(field_name='bid_date', lookup_expr='lte')

    def filter_q(self, qs, name, q):
        return qs.filter(pk__in=FtsTengator.objects.search(q))

    def filter_hot_lots(self, qs, name, q):
        return qs.filter(has_request=False, bid_date__lte=datetime.now() + timedelta(days=2))

    class Meta:
        model = Lot
        fields = [
            'q', 'hot_lots', 'region', 'area', 'category', 'sub_category', 'bid_date', 'has_request',
            'start_price_from', 'start_price_to', 'bid_date_from', 'bid_date_to'
        ]
