from rest_framework import serializers

from aggregator.models import Lot


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
