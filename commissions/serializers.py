from rest_framework import serializers
from .models import Sales, Salesperson
from authentication.serializers import User, UserSerializer 
from django.db.models import Sum

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class SalespersonSeralizer(serializers.ModelSerializer):
    
    class Meta:
        model = Salesperson
        fields = '__all__'

class SalespersonDetailSerializer(serializers.ModelSerializer):
    sponser = serializers.SerializerMethodField()

    class Meta:
        model = Salesperson
        fields = '__all__'

    def get_sponser (self, obj):
        if obj is None:
            sponser = Salesperson.objects.get(id=obj.sponser.id)
            serializer = SalespersonSeralizer(sponser)
            return serializer.data
        else:
            return None
