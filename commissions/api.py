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
            username=request.data["username"],
            first_name= request.data["name"],
            email=request.data["email"]
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

    # When updating and creating sales update the related salesperson as well
    def create(self, request):
        response = super().create(request)
        print(response.data)
        salesperson = Salesperson.objects.get(id = response.data["salesperson"])
        salesperson.total_individual_sales += response.data["total"]
        salesperson.total_individual_commission += response.data["commission_perc"]
        salesperson.save()
        # Then update commission for all related salesperson
        return response

    def update(self, request, pk):
        oldsale = Sales.objects.get(id= pk)
        response = super().update(request, pk)
        # Handle salesperson change
        salesperson = Salesperson.objects.get(id = response.data["salesperson"])
        salesperson.total_individual_sales += (response.data["total"] - oldsale.total)
        salesperson.total_individual_commission += (response.data["commission_perc"] - oldsale.commission_perc)
        salesperson.save()       
        return response

    def destroy(self, request, pk):
        oldsale = Sales.objects.get(id = pk)
        salesperson = Salesperson.objects.get(id= oldsale.salesperson.id)
        salesperson.total_individual_sales -= oldsale.total
        salesperson.total_individual_commission -= oldsale.commission_perc
        salesperson.save()
        response = super().destroy(request, pk)
        return response

# Method to calculate all related commissions when a salesperson is given