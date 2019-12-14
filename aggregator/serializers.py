from rest_framework import serializers

from aggregator.models import Lot


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = [
            'id', 'bid_date', 'bid_id', 'region', 'area', 'title', 'start_price', 'conditions', 'customer_info',
            'description', 'url'
        ]
