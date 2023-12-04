# ecommerce_app/serializers.py

from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem
from rest_framework.validators import UniqueValidator
import random,datetime

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': [UniqueValidator(queryset=Customer.objects.all())]}, 
            'email': {'validators': []}, 
        }

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': [UniqueValidator(queryset=Product.objects.all())]},
            'weight': {'max_value': 25, 'min_value': 0}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_number', 'customer', 'order_date', 'address', 'order_items']

 


    def validate_order_date(self, value):
        if value and value < datetime.date.today():
            raise serializers.ValidationError("Order Date cannot be in the past.")
        return value

    def validate(self, data):
        order_items_data = data.get('order_items', [])

        total_weight = sum(item_data['product'].weight * item_data['quantity'] for item_data in order_items_data)

        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")

        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])

        last_order_number = Order.objects.all().order_by('-order_number').first()
        if last_order_number:
            current_number_str = ''.join(filter(str.isdigit, last_order_number.order_number))
            current_number = int(current_number_str) + 1
        else:
            current_number = 1

        order_number = f'ORD{current_number:05d}'
        validated_data["order_number"] = order_number

        order_items = order_items_data  
        order = Order.objects.create(**validated_data)

        for order_item_data in order_items:
            OrderItem.objects.create(order=order, **order_item_data)

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')

        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)

        self.validate_order_date(instance.order_date)

        total_weight = sum(item_data['product'].weight * item_data['quantity'] for item_data in order_items_data)

        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")

        OrderItem.objects.filter(order=instance).delete()
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=instance, **order_item_data)

        instance.save()
        return instance
