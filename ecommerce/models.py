from enum import Enum, auto

from django.db import models
from enumchoicefield import EnumChoiceField
from rest_framework.exceptions import ValidationError

from ecommerce.utils import validate_product_ids_and_quantities


# Create your models here.


class OrderState(Enum):
    PENDING = auto()
    COMPLETED = auto()


class Product(models.Model):
    name = models.CharField(help_text="Name of the Product")
    description = models.TextField(help_text="Description of the Product", null=True, blank=True)
    price = models.FloatField(help_text="Price of the Product")
    stock = models.PositiveIntegerField(help_text="Available Quantities of the Product")

    def __str__(self) -> str:
        return f"Product ID: {self.id}, Name: {self.name}, Price: {self.price}, Stock: {self.stock}"


class Order(models.Model):
    """
    products field value format:
        {
            product_id: quantities
        }
    """
    products = models.JSONField(help_text="Mapping of Product id and it's quantities")
    status = EnumChoiceField(OrderState, default=OrderState.PENDING, help_text="Shows the current state of Order")

    def __str__(self) -> str:
        return f"Order ID: {self.id}, Status: {self.status.name}"

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        output_data = validate_product_ids_and_quantities(product_quantity_mapping=self.products)
        if not output_data.get('is_success'):
            raise ValidationError(output_data)
        return super().full_clean(exclude=exclude, validate_unique=validate_unique,
                                  validate_constraints=validate_constraints)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super().save(*args,force_insert, force_update, using, update_fields)


class SizeChoiceEnum(Enum):
    MEDIUM = auto()
    LARGE = auto()
    SMALL = auto()

class Menu(models.Model):
    name = models.CharField(max_length=25, help_text='Name of the dish')
    size = EnumChoiceField(SizeChoiceEnum, help_text='Size of the dish', default=SizeChoiceEnum.SMALL)
    price = models.FloatField(help_text='Price of the dish')
    toppings = models.ManyToManyField("Topping")

class Topping(models.Model):
    name = models.CharField(max_length=50, help_text='Name of the topping')

