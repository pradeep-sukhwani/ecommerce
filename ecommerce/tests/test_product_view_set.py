from rest_framework import status
from rest_framework.status import HTTP_200_OK
from .base_test import EcommerceTestBase
from ..models import Product


class ProductTestCase(EcommerceTestBase):

    def test_get_product(self):
        product_queryset = Product.objects.all()
        response = self.client.get(path=self.product_api_view_set_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        for data in response.data:
            product_object = product_queryset.get(id=data.get('id'))
            self.assertIsNotNone(product_object)
            self.assertEqual(data.get("id"), product_object.id)
            self.assertEqual(data.get("name"), product_object.name)
            self.assertEqual(data.get("description"), product_object.description)
            self.assertEqual(data.get("price"), product_object.price)
            self.assertEqual(data.get("stock"), product_object.stock)

    def test_get_product_by_id(self):
        product_object = Product.objects.all().first()
        response = self.client.get(path=f"{self.product_api_view_set_url}{product_object.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get("id"), product_object.id)
        self.assertEqual(response.data.get("name"), product_object.name)
        self.assertEqual(response.data.get("description"), product_object.description)
        self.assertEqual(response.data.get("price"), product_object.price)
        self.assertEqual(response.data.get("stock"), product_object.stock)


    def test_update_product(self):
        product_object = Product.objects.all().first()
        payload = {
            "description": "New Updated Sample Test Description",
        }
        response = self.client.patch(path=f"{self.product_api_view_set_url}{product_object.id}/",
                                     data=payload, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('id'), product_object.id)
        self.assertEqual(response.data.get('description'), payload.get('description'))
        product_object.refresh_from_db()
        self.assertEqual(product_object.description, payload.get('description'))
