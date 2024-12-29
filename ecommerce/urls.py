from sys import prefix

from django.urls import re_path, include
from rest_framework import routers

from .views import ProductViewSet, OrderViewSet

router = routers.DefaultRouter()


router.register(prefix=r'product', viewset=ProductViewSet)
router.register(prefix=r'order', viewset=OrderViewSet)

urlpatterns = [re_path(r"^", include(router.urls))]
