from django.urls import path

from aggregator.views import LotListAPIView

urlpatterns = [
    path('lots/', LotListAPIView.as_view(), name='lot-list'),
]
