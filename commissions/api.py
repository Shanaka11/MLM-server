from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SalespersonSeralizer, SalesSerializer
from .models import Sales, Salesperson

class SalespersonApi(viewsets.ModelViewSet):
    queryset = Salesperson.objects.all()
    serializer_class = SalespersonSeralizer
    # When Creating Salesperson create a user as well if password is not given set a default password

class SalesApi(viewsets.ModelViewSet):
    queryset= Sales.objects.all()
    serializer_class = SalesSerializer