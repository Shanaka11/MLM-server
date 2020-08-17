from rest_framework import serializers
from .models import Sales, Salesperson
from authentication.serializers import User, UserSerializer 
from django.db.models import Sum

class SalesSerializer(serializers.ModelSerializer):
    # CPF
    salesperson_cpf = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Sales
        fields = '__all__'

    def get_salesperson_cpf(self, obj):
        salesperson = Salesperson.objects.get(id=obj.salesperson.id)
        return salesperson.user.username

class SalespersonSeralizer(serializers.ModelSerializer):
    sponser_cpf = serializers.SerializerMethodField(read_only = True)    
    salesperson_cpf = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Salesperson
        fields = '__all__'

    def get_sponser_cpf(self, obj):
        if obj.sponser is not None:
            salesperson = Salesperson.objects.get(id=obj.sponser.id)
            return salesperson.user.username         
        else:
            return None

    def get_salesperson_cpf(self, obj):
        return obj.user.username

class SalespersonDetailSerializer(serializers.ModelSerializer):
    sponser = serializers.SerializerMethodField()
    sponser_cpf = serializers.SerializerMethodField(read_only = True)

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

    def get_sponser_cpf(self, obj):
        salesperson = Salesperson.objects.get(id=obj.sponser.id)
        return salesperson.user.username            
