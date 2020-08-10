from rest_framework import serializers
from .models import Sales, Salesperson
from django.db.models import Sum

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class SalespersonSeralizer(serializers.ModelSerializer):
    # Total individual sales
    # Total group sales 
    # total_group_sales = serializers.SerializerMethodField(read_only = true)
    total_individual_sales = serializers.SerializerMethodField(read_only = True)
    get_total_individual_commission = serializers.SerializerMethodField(read_only = True)
    # individual_commission
    # group_commission
    
    class Meta:
        model = Salesperson
        fields = '__all__'

    # def get_total_group_sales (self, obj):
    #     sales = Sales.objects.filter(salesperson=obj)

    def get_total_individual_sales (self, obj):
        sales = Sales.objects.filter(salesperson_id=obj.id)
        total = sales.aggregate(Sum('total'))
        if total['total__sum'] is None:
            total['total__sum'] = 0
        # serializer = SalesSerializer(sales, many=True)
        # return serializer.data
        return total['total__sum']

    def get_total_individual_commission (self, obj):
        sales = Sales.objects.filter(salesperson_id=obj.id)
        total = sales.aggregate(Sum('commission_perc'))
        if total['commission_perc__sum'] is None:
            total['commission_perc__sum'] = 0
        return total['commission_perc__sum']

    # def get_total_group_sales (self, obj):

    # def get_total_group_commission(self, obj)
