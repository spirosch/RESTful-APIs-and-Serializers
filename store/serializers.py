from unittest.util import _MAX_LENGTH
from rest_framework import serializers

# this class will inherit this serializer class that is defined
# in the module (import serializers)
# So the serializers module that we imported here it has a Serializer class

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
