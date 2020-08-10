from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SalespersonSeralizer, SalesSerializer, SalespersonDetailSerializer
from .models import Sales, Salesperson
from authentication.serializers import  User, UserProfile, Role

class SalespersonApi(viewsets.ModelViewSet):
    queryset = Salesperson.objects.all()
    serializer_class = SalespersonSeralizer    

    def retrieve(self, request, pk):
        response = super().retrieve(request, pk)
        sponser = Salesperson.objects.get(id=response.data["sponser"])
        response.data["sponser"] = SalespersonSeralizer(sponser).data
        return response

    def create(self, request):
        # When Creating Salesperson create a user as well if password is not given set a default password
        user = User.objects.create(
            username=request.data["name"],
            first_name= request.data["name"],
            # email=request.data["email"]
        )
        user.set_password("MiguelIsGood")
        user.save()
        request.data['user'] = user.id
        # Create Salesperson
        response = super().create(request)
        # Create user profile
        role = Role.objects.get(role = "CLIENT")
        user_profile = UserProfile.objects.create(
            user = user,
            role = role
        )
        return response

class SalesApi(viewsets.ModelViewSet):
    queryset= Sales.objects.all()
    serializer_class = SalesSerializer