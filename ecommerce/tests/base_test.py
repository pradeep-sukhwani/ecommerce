import json
import os
from rest_framework.test import APITestCase

from ecommerce.models import Product, Order


class EcommerceTestBase(APITestCase):
    def setup_mock_data(self):
        product_data_list = json.load(open(os.path.join(os.path.dirname(__file__), "fixtures", "products.json")))
        order_data_list = json.load(open(os.path.join(os.path.dirname(__file__), "fixtures", "orders.json")))
        product_list = []
        order_list = []
        for product_data in product_data_list:
            product_list.append(Product(**product_data))
        for order_data in order_data_list:
            order_list.append(Order(**order_data))

        Product.objects.bulk_create(product_list)
        Order.objects.bulk_create(order_list)

    def setUp(self):
        # Load Products fixtures
        # Create Sample Products
        self.setup_mock_data()
        self.product_api_view_set_url = "/api/product/"
        self.order_api_view_set_url = "/api/order/"
