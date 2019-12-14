from rest_framework import serializers

from aggregator.models import Lot, Region, Area, Category, SubCategory


class LotListSerializer(serializers.ModelSerializer):
    def to_representation(self, lot):
        data = super().to_representation(lot)
        data['region'] = lot.region.title
        data['area'] = lot.area.title
        data['category'] = lot.category.title
        data['sub_category'] = ', '.join([sub_category.title for sub_category in lot.sub_category.all()])
        return data

    class Meta:
        model = Lot
        fields = [
            'id', 'bid_date', 'bid_id', 'region', 'area', 'category', 'sub_category', 'title', 'start_price',
            'conditions', 'customer_info', 'description', 'url', 'has_request'
        ]


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'title']


class RegionSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'title', 'areas']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'sub_categories']


class FilterDataSerializer(serializers.Serializer):
    regions = RegionSerializer(many=True)
    categories = CategorySerializer(many=True)
