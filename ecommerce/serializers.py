from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, Order, OrderState


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

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
        return data
