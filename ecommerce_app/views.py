from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from django.db.models import Q

class NoOrdersFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'No orders found for the provided products.'

class NoCustomerFound(APIException):
    status_code=status.HTTP_404_NOT_FOUND
    default_detail= "No orders found for the provided Customer"


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        product_names = self.request.query_params.get('products', '')
        customer_name = self.request.query_params.get('customer', '')
        

        if product_names:
            product_names_list = product_names.split(',')
            queryset = queryset.filter(order_items__product__name__in=product_names_list).distinct()

            if not queryset.exists():
                raise NoOrdersFound

        if customer_name:
            
            queryset = queryset.filter(Q(customer__name__iexact=customer_name)).distinct()

            if not queryset.exists():
                raise NoCustomerFound

        return queryset

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
