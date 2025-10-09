from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
import inspect

router = DefaultRouter()

for name, cls in inspect.getmembers(views):
    if 'ViewSet' in name:
        prefix = name.replace('ViewSet', '').lower()
        # 规则：BlogViewSet → ''
        if prefix == 'blog':
            prefix = ''
        router.register(prefix, cls)

urlpatterns = [
    # Include all router URLs
    path('', include(router.urls)),
]
