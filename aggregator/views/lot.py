from datetime import datetime

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from aggregator.filtersets import LotFilter
from aggregator.models import Lot, Region, Category
from aggregator.serializers.lot import LotListSerializer, FilterDataSerializer
from aggregator.utils.pagination import StandardResultsSetPagination


class LotListAPIView(ListAPIView):
    serializer_class = LotListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filterset_class = LotFilter
    queryset = Lot.objects.filter(bid_date__gte=datetime.now()).select_related('region', 'area').order_by()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset


class LotDetailAPIView(ListAPIView):
    serializer_class = LotListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filterset_class = LotFilter
    queryset = Lot.objects.filter(bid_date__gte=datetime.now()).order_by('-id').select_related('region', 'area')


class FilterDataAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        return {
            'regions': Region.objects.all().prefetch_related('areas'),
            'categories': Category.objects.all().prefetch_related('sub_categories'),
        }

    def get(self, request, *args, **kwargs):
        return Response(FilterDataSerializer(instance=self.get_queryset()).data)
