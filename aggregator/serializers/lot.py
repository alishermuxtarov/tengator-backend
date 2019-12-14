from rest_framework import serializers

from aggregator.models import Lot, Region, Area, Category, SubCategory


class LotListSerializer(serializers.ModelSerializer):
    def to_representation(self, lot):
        data = super().to_representation(lot)
        data['region'] = lot.region.title
        data['area'] = lot.area.title
        return data

    class Meta:
        model = Lot
        fields = [
            'id', 'bid_date', 'bid_id', 'region', 'area', 'title', 'start_price', 'conditions', 'customer_info',
            'description', 'url'
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
