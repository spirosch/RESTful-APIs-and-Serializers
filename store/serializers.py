from dataclasses import fields
from decimal import Decimal
from multiprocessing import context
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from store.models import Product, Collection

# this class will inherit this serializer class that is defined
# in the module (import serializers)
# So the serializers module that we imported here it has a Serializer class


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']
    # id = serializers.IntegerField()
    # title= serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(), 
    #     view_name='collection-detail',
    # )

       


    def calculate_tax (self, product: Product):
        return product.unit_price * Decimal(1.1)