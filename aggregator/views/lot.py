from datetime import datetime

from django.db.models import Value
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from aggregator.filtersets import LotFilter
from aggregator.models import Lot, Region, Category, SubCategory
from aggregator.serializers.lot import LotListSerializer, FilterDataSerializer, CategoryReportSerializer
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


class SuggestAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q', '')
        results = []
        if q and q != '':
            categories = Category.objects.filter(
                title__icontains=q
            ).annotate(order=Value(1)).values('title')
            sub_categories = SubCategory.objects.filter(
                title__icontains=q
            ).annotate(order=Value(2)).values('title')
            results = [category.get('title') for category in categories.union(sub_categories)[:10]]
        return Response(results)


class CategoriesReportAPIView(ListAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    serializer_class = CategoryReportSerializer
    queryset = Lot.objects.categories_report()
