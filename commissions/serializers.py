from rest_framework import serializers
from .models import Sales, Salesperson

class SalespersonSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Salesperson
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'