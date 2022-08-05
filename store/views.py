from ast import Return
from itertools import count
from multiprocessing import context
from os import stat
from turtle import title
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, OrderItem, Product
from .serializers import CollectionSerializer, ProductSerializer
from store import serializers
from django.db.models.aggregates import Count 
# Create your views here.


class ProductList(APIView):
    def get (self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request':request})
        return Response(serializer.data)
    def post (self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print (serializer.validated_data)
        return Response (serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get (self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put (self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete (self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count()>0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'}
            , status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#          serializer = ProductSerializer(data=request.data)
#          serializer.is_valid(raise_exception=True)
#          serializer.save()
#          print (serializer.validated_data)
#          return Response (serializer.data, status=status.HTTP_201_CREATED)
         
        #  serializer.validated_data
        #  return Response ('ok')

# @api_view(['GET', 'PUT','DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count()>0:
#             return Response(
#                 {'error': 'Product cannot be deleted because it is associated with an order item.'}
#             , status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all().order_by('id')
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response (serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT','DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')) , pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 
            'Collection cannot be deleted because it is associate with one or more products'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





        





