from django.contrib import admin
from aggregator import models


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['bid_id', 'bid_date', 'region', 'area', 'title', 'start_price']
    search_fields = ['conditions', 'customer_info', 'title', 'bid_id']
    list_filter = ['bid_date']


@admin.register(models.SearchWord)
class LotAdmin(admin.ModelAdmin):
    list_display = ['word', 'user']
    search_fields = ['word']


