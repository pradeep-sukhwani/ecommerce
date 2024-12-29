from parameterized import parameterized
from rest_framework import status

from .base_test import EcommerceTestBase
from ..models import Order, OrderState, Product
from ..utils import process_order


class OrderTestCase(EcommerceTestBase):

    def test_get_order(self):
        order_queryset = Order.objects.all()
        response = self.client.get(path=self.order_api_view_set_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        for data in response.data:
            order_object = order_queryset.get(id=data.get('id'))
            self.assertIsNotNone(order_object)
            self.assertEqual(data.get("id"), order_object.id)
            self.assertEqual(data.get("status"), order_object.status.name)

    def test_get_order_by_id(self):
        order_object = Order.objects.all().first()
        response = self.client.get(path=f"{self.order_api_view_set_url}{order_object.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(order_object)
        self.assertEqual(response.data.get("id"), order_object.id)
        self.assertEqual(response.data.get("status"), order_object.status.name)

    @parameterized.expand([
        [{1000: 1}, "invalid_product_ids", status.HTTP_400_BAD_REQUEST],
        [{1: 1000, 3: 6}, "product_ids_quantity_mismatch", status.HTTP_400_BAD_REQUEST],
        [{1: 6, 3: 6}, None, status.HTTP_201_CREATED],
    ])
    def test_create_order(self, payload, error_field, status_code):
        response = self.client.post(path=self.order_api_view_set_url, data={"products": payload}, format='json')
        self.assertEqual(response.status_code, status_code)
        if error_field:
            self.assertIsNotNone(response.data.get(error_field))
        else:
            self.assertIsNotNone(response.data)
            self.assertIsNotNone(response.data.get('id'))
            self.assertIsNotNone(response.data.get('products'))
            self.assertEqual(response.data.get('status'), OrderState.PENDING.name)

    @parameterized.expand([
        [{"products": {1000: 1}}, "invalid_product_ids", status.HTTP_400_BAD_REQUEST],
        [{"products": {1: 1000, 3: 6}}, "product_ids_quantity_mismatch", status.HTTP_400_BAD_REQUEST],
        [{"products": {1: 1000, 3: 6}, "status": "COMPLETED"}, "status", status.HTTP_400_BAD_REQUEST],
        [{"products": {1: 1, 3: 6}}, "error", status.HTTP_400_BAD_REQUEST],
        [{"products": {1: 6, 3: 6}}, None, status.HTTP_200_OK],
    ])
    def test_update_order(self, payload, error_field, status_code):
        order_object = Order.objects.all().first()
        if error_field == 'error':
            # We are trying update a processed order
            order_object = process_order(order_object)
            order_object.refresh_from_db()
        response = self.client.patch(path=f"{self.order_api_view_set_url}{order_object.id}/",
                                     data=payload, format='json')
        self.assertEqual(response.status_code, status_code)
        if error_field:
            self.assertIsNotNone(response.data.get(error_field))
        else:
            self.assertIsNotNone(response.data)
            self.assertIsNotNone(response.data.get('id'))
            self.assertIsNotNone(response.data.get('products'))
            self.assertEqual(response.data.get('status'), OrderState.PENDING.name)

    def test_process_order_failure_processed_completed_order(self):
        """
        Case when we are processing the completed order
        """
        order_object = Order.objects.filter(status=OrderState.PENDING).first()
        # First time Processing order
        process_order(order_object)
        # Processing order again
        response = self.client.patch(path=f"{self.order_api_view_set_url}{order_object.id}/process_order/",
                                     format='json')
        self.assertIsNotNone(response.data.get('error'))
        self.assertEqual(response.data.get('error'), "Order is already processed")

    def test_process_order_failure_quantities_not_available(self):
        """
        Case when we are processing order but quantities are no longer available
        """
        order_object = Order.objects.filter(status=OrderState.PENDING).first()
        # Get product id from products field
        product_id = list(order_object.products.keys())[0]
        # Update available stock to 0
        Product.objects.filter(id=product_id).update(stock=0)
        # Processing order
        response = self.client.patch(path=f"{self.order_api_view_set_url}{order_object.id}/process_order/",
                                     format='json')
        self.assertFalse(response.data.get('is_success'))
        self.assertIsNotNone(response.data.get('product_ids_quantity_mismatch'))
