from sys import prefix

from django.urls import re_path, include
from rest_framework import routers

from .views import ProductViewSet, OrderViewSet, MenuViewSet

router = routers.DefaultRouter()


router.register(prefix=r'product', viewset=ProductViewSet)
router.register(prefix=r'order', viewset=OrderViewSet)
router.register(prefix=r'menu', viewset=MenuViewSet)

urlpatterns = [re_path(r"^", include(router.urls))]
