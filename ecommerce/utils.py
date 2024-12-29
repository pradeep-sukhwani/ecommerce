from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError


def validate_product_ids_and_quantities(product_quantity_mapping: dict) -> dict:
    # Importing locally to avoid circular import error
    from ecommerce.models import Product
    product_ids = product_quantity_mapping.keys()
    available_product_ids = Product.objects.filter(id__in=product_ids).values_list("id", flat=True)
    output_data = {"is_success": True}

    # Check if product ids are valid or not
    if len(product_ids) != len(available_product_ids):
        output_data.update({"is_success": False,
                            "invalid_product_ids": set(product_ids).difference(set(available_product_ids))})
        return output_data

    # Check if required quantities are available or not
    product_id_available_quantity_mapping = {}
    for product_id, asked_quantity in product_quantity_mapping.items():
        product_object = Product.objects.get(id=product_id)
        if asked_quantity > product_object.stock:
            product_id_available_quantity_mapping.update({product_id: {"available_quantity": product_object.stock,
                                                                       "asked_quantity": asked_quantity}})
    if product_id_available_quantity_mapping:
        output_data.update({"product_ids_quantity_mismatch": product_id_available_quantity_mapping,
                            "is_success": False})
    return output_data


def process_order(order_object):
    # Importing locally to avoid circular import error
    from ecommerce.models import Product, OrderState
    with transaction.atomic():
        for product_id, asked_quantity in order_object.products.items():
            Product.objects.filter(id=product_id).update(stock=F('stock') - asked_quantity)
        order_object.status = OrderState.COMPLETED
        order_object.save(update_fields=['status'])
        order_object.refresh_from_db()
    return order_object
