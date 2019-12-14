from django.urls import path, include

from aggregator.views.auth import LoginView
from aggregator.views.lot import LotListAPIView, FilterDataAPIView

urlpatterns = [
    path('auth/', include([
        path('login/', LoginView.as_view(), name='login'),
    ])),
    path('aggregator/', include([
        path('lots/', LotListAPIView.as_view(), name='lot-list'),
        path('filter_data/', FilterDataAPIView.as_view(), name='filter-data'),
    ])),
]
