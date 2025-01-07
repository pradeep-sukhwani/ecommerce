from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ecommerce.models import Product, Order, OrderState, Menu
from ecommerce.serializers import ProductSerializer, OrderSerializer, MenuSerializer
from ecommerce.utils import process_order, validate_product_ids_and_quantities


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    """
    GET:
        List of all Products: /api/product/
        Get a particular Product by ID: /api/product/{product_id}
    POST:
        Create a new product: /api/product/
        Payload:
            `name`: <str>: "Sample Product 1"
            `description`: <str>: "Sample Description"
            `price`: <float>: 6.1
            `stock`: <int>: 5
        Response:
            Serialized object of Product
    PATCH:
        Update an existing product: /api/product/{product_id}/
        Payload (Fields that can be updated):
            `name`: <str>: "Updated Sample Product 1"
            `description`: <str>: "Updated Sample Description"
            `price`: <float>: 1.6
            `stock`: <int>: 4
        Response:
            Serialized object of Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "id"  # This is used to get the id from the url and pass it to the get_object method.
    http_method_names = ["get", "post", "patch"]


class OrderViewSet(viewsets.ModelViewSet):
    """
    GET:
        List of all Orders: /api/order/
        Get a particular order by ID: /api/order/{order_id}
    POST:
        Create a new order: /api/order/
        Payload:
            `products`: <dict>: {1: 10}
                Here, 1 is the product id and 10 is the quantity of that product.
            By default, the order status will be PENDING
        Response:
            Error if product is not valid or asked quantity is not available else serialized object of Order
    PATCH:
        Update an existing order: /api/order/{order_id}/
        Payload:
            `products`: <dict>: {1: 11, 2: 5}
                Here, 1 is an existing product id with updated quantity as 11 and 2 is the new product id with its
                quantity as 5.
            By default, the order status will be PENDING
        Response:
            Error if product is not valid or asked quantity is not available else serialized object of Order

        process an existing order: /api/order/{order_id}/process_order/
        Payload:
            order_id: <int>: 1
        Response:
            Error if Order is already Completed else serialized object of Order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "id"  # This is used to get the id from the url and pass it to the get_object method.
    http_method_names = ["get", "post", "patch"]


    @action(detail=True, methods=["patch"])
    def process_order(self, request, *args, **kwargs):
        """
        This view is used to process an existing order
        """
        order_object = self.get_object()
        output_data = validate_product_ids_and_quantities(order_object.products)
        if not output_data.get("is_success"):
            return Response(output_data, status=status.HTTP_400_BAD_REQUEST)
        if order_object.status == OrderState.COMPLETED:
            return Response({"error": "Order is already processed"}, status=status.HTTP_400_BAD_REQUEST)
        order_object = process_order(order_object=order_object)
        serializer = self.get_serializer(order_object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Menu.objects.all()
    lookup_url_kwarg = "name"
    serializer_class = MenuSerializer

    def get_queryset(self):
        current_query_set = super().get_queryset()
        if self.request.query_params:
            return current_query_set.filter(name=self.request.query_params.get('name'))
        return current_query_set
