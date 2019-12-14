from datetime import datetime

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from aggregator.filtersets import LotFilter
from aggregator.models import Lot
from aggregator.serializers.lot import LotListSerializer
from aggregator.utils.pagination import StandardResultsSetPagination


class LotListAPIView(ListAPIView):
    serializer_class = LotListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filterset_class = LotFilter
    queryset = Lot.objects.filter(bid_date__gte=datetime.now()).order_by('-id').select_related('region', 'area')