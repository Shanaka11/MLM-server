from django.shortcuts import render
from .models import Salesperson, Sales
from .serializers import SalespersonSeralizer, SalesSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(('GET',))
def getConnectedSalesperson(request, id):
    salespersons = Salesperson.objects.filter(sponser_id = id)
    serializer = SalespersonSeralizer(salespersons , many=True)
    return Response(serializer.data, status=200)

@api_view(('GET',))
def searchSalesperson(response, name):
    salespersons = Salesperson.objects.filter(name__icontains = name)    
    serializer = SalespersonSeralizer(salespersons , many=True)
    return Response(serializer.data, status=200)

@api_view(('GET', ))
def searchSales(response, name):
    sales = Sales.objects.filter(salesperson__id__icontains = name)
    serializer = SalesSerializer(sales, many=True)
    return Response(serializer.data, status=200)