from .base_test import EcommerceTestBase
from parameterized import parameterized

from ecommerce.models import Product, Order, OrderState
from ecommerce.utils import validate_product_ids_and_quantities, process_order


class UtilTestCase(EcommerceTestBase):
    @parameterized.expand([
        ["invalid_product_ids"],
        ["product_ids_quantity_mismatch"],
        [None],
    ])
    def test_validate_product_ids_and_quantities(self, error_type):
        if error_type == 'invalid_product_ids':
            # Case where product ids are incorrect
            product_id_quantity_mapping = {
                1000: 2000, 2000: 3000
            }
            output_data = validate_product_ids_and_quantities(product_id_quantity_mapping)
            self.assertFalse(output_data.get("is_success"))
            self.assertIsNotNone(output_data.get("invalid_product_ids"))
            self.assertIsNone(output_data.get("product_ids_quantity_mismatch"))
        elif error_type == 'product_ids_quantity_mismatch':
            # Case where product ids are correct but asked quantities are more than available quantities
            available_product_ids = Product.objects.all().values_list("id", flat=True)
            product_id_quantity_mapping = {product_id: 1000 for product_id in available_product_ids}
            output_data = validate_product_ids_and_quantities(product_id_quantity_mapping)
            self.assertFalse(output_data.get("is_success"))
            self.assertIsNone(output_data.get("invalid_product_ids"))
            self.assertIsNotNone(output_data.get("product_ids_quantity_mismatch"))
        else:
            # Case where both product ids are correct and asked quantity are available
            available_product_data = Product.objects.all().values("id", "stock")
            product_id_quantity_mapping = {product_data.get("id"): product_data.get("stock") for product_data in
                                           available_product_data}
            output_data = validate_product_ids_and_quantities(product_id_quantity_mapping)
            self.assertTrue(output_data.get("is_success"))
            self.assertIsNone(output_data.get("invalid_product_ids"))
            self.assertIsNone(output_data.get("product_ids_quantity_mismatch"))

    def test_process_order_success(self):
        order_object = Order.objects.filter(status=OrderState.PENDING).first()
        response = process_order(order_object)
        self.assertEqual(response.status, OrderState.COMPLETED)
