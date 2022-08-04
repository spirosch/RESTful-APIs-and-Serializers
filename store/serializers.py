from decimal import Decimal
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from store.models import Product, Collection

# this class will inherit this serializer class that is defined
# in the module (import serializers)
# So the serializers module that we imported here it has a Serializer class

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.StringRelatedField()
       


    def calculate_tax (self, product: Product):
        return product.unit_price * Decimal(1.1)