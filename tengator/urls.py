from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('docs/', include_docs_urls(title='Tengator API Documentation', permission_classes=[])),
        path('', include(('aggregator.urls', 'aggregator'), namespace='aggregator')),
    ])),
]
