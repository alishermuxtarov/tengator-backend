from django_filters import rest_framework as filters

from aggregator.models import Lot, FtsTengator


class LotFilter(filters.FilterSet):
    q = filters.CharFilter(method='filter_q')

    def filter_q(self, qs, name, q):
        return qs.filter(pk__in=FtsTengator.objects.search(q))

    class Meta:
        model = Lot
        fields = ['q']
