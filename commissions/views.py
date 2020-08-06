from django.shortcuts import render
from .models import Salesperson
from .serializers import SalespersonSeralizer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(('GET',))
def getConnectedSalesperson(request, id):
    salespersons = Salesperson.objects.filter(sponser_id = id)
    serializer = SalespersonSeralizer(salespersons , many=True)
    return Response(serializer.data, status=200)
    