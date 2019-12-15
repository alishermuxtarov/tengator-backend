from django.urls import path, include

from aggregator.views.auth import LoginView, SignInView, ConfirmationView
from aggregator.views.lot import LotListAPIView, FilterDataAPIView, LotDetailAPIView, SuggestAPIView

urlpatterns = [
    path('auth/', include([
        path('login/', LoginView.as_view(), name='login'),
        path('signin/', SignInView.as_view(), name='signin'),
        path('confirm/', ConfirmationView.as_view(), name='confirm'),
    ])),
    path('aggregator/', include([
        path('lots/', LotListAPIView.as_view(), name='lot-list'),
        path('lots/<int:pk>/', LotDetailAPIView.as_view(), name='lot-detail'),
        path('filter_data/', FilterDataAPIView.as_view(), name='filter-data'),
        path('suggest/', SuggestAPIView.as_view(), name='suggest'),
    ])),
]
