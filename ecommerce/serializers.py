from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, Order, OrderState, Menu, Topping


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', "price", "products")

    def get_price(self, object):
        products = object.products
        price = 0.0
        for product_id, quantity in products.items():
            product_object = Product.objects.get(id=product_id)
            price += product_object.price * quantity
        return price

    def validate(self, attrs):
        # Status cannot be updated at the time of placing or updating an order
        if attrs.get("status"):
            raise ValidationError({"status": "Status cannot be updated"})
        return attrs

    def update(self, instance, validated_data):
        # Cannot update order once it is in processed
        if instance.status == OrderState.COMPLETED:
            raise ValidationError({"error": "Processed Order cannot be updated"})
        return super().update(instance=instance, validated_data=validated_data)

    def to_representation(self, instance) -> dict:
        data = super(OrderSerializer, self).to_representation(instance=instance)
        data["status"] = instance.status.name
        data.pop("products")
        return data


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ("name",)


class MenuSerializer(serializers.ModelSerializer):
    toppings = ToppingSerializer(many=True)

    class Meta:
        model = Menu
        fields = "__all__"
