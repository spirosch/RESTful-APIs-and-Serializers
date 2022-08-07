from dataclasses import field, fields
from decimal import Decimal
from itertools import product
from multiprocessing import context
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from store.models import Product, Collection, Review


# this class will inherit this serializer class that is defined
# in the module (import serializers)
# So the serializers module that we imported here it has a Serializer class


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


    # id = serializers.IntegerField()
    # title= serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'slug', 'inventory', 
        'unit_price', 'price_with_tax', 'collection']
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

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
        
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
        
    # def validate(self, data):
    #     if data ['password'] != data ['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data
    # So here if the password do not match with the confirm password then, client get an error message, 
    # else return data (which is a dictionary. This doesn’t make sense in our content so this is just an 
    # example in a situation like this.



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

    