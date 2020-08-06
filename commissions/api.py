from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SalespersonSeralizer, SalesSerializer
from .models import Sales, Salesperson
from authentication.serializers import  User, UserProfile, Role

class SalespersonApi(viewsets.ModelViewSet):
    queryset = Salesperson.objects.all()
    serializer_class = SalespersonSeralizer    

    def create(self, request):
        response = super().create(request)
        # When Creating Salesperson create a user as well if password is not given set a default password
        user = User.objects.create(
            username=request.data["name"],
            first_name= request.data["name"],
            # email=request.data["email"]
        )
        user.set_password("MiguelIsGood")
        user.save()
        # Create user profile
        role = Role.objects.get(role = "ADMIN")
        user_profile = UserProfile.objects.create(
            user = user,
            role = role
        )
        return response
class SalesApi(viewsets.ModelViewSet):
    queryset= Sales.objects.all()
    serializer_class = SalesSerializer