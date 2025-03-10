from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SalespersonSeralizer, SalesSerializer, SalespersonDetailSerializer
from .models import Sales, Salesperson
from authentication.serializers import  User, UserProfile, Role

from django.db.models import Sum
from django.db import transaction

class SalespersonApi(viewsets.ModelViewSet):
    queryset = Salesperson.objects.all()
    serializer_class = SalespersonSeralizer    

    def retrieve(self, request, pk):
        response = super().retrieve(request, pk)
        if response.data["sponser"]:
            sponser = Salesperson.objects.get(id=response.data["sponser"])
            response.data["sponser"] = SalespersonSeralizer(sponser).data
        return response

    @transaction.atomic
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
        try:
            sponser_user = User.objects.get(username = request.data["sponser"])
            request.data["sponser"] = sponser_user.salesperson.id
        except:
            pass
        request.data["qualification"] = 0
        response = super().create(request)
        # Create user profile
        role = Role.objects.get(role = "CLIENT")
        user_profile = UserProfile.objects.create(
            user = user,
            role = role,
            cell = request.data["cell"]
        )
        try:
            response.data["sponser"] = sponser_user.salesperson.id
        except:
            pass
        return response

class SalesApi(viewsets.ModelViewSet):
    queryset= Sales.objects.all()
    serializer_class = SalesSerializer

    # When updating and creating sales update the related salesperson as well
    @transaction.atomic
    def create(self, request):
        # In our case salespersonID = salesperson username    
        user = User.objects.get(username = request.data["salesperson"])
        request.data["salesperson"] = user.salesperson.id

        response = super().create(request)    

        salesperson = Salesperson.objects.get(id = response.data["salesperson"])
        salesperson.total_individual_sales += response.data["total"]
        salesperson.total_individual_commission += response.data["commission_perc"]
        salesperson.save()
        # Then update commission for all related salesperson
        UpdateDirectCommission(salesperson, 0)
        UpdateGroupCommissions(salesperson)
        UpdateGroupCommissionsBasic(salesperson, response.data["total"])

        response.data["salesperson"] = user.salesperson.id

        return response

    @transaction.atomic
    def update(self, request, pk):
        oldsale = Sales.objects.get(id= pk)
        # In our case salespersonID = salesperson username            
        user = User.objects.get(username = request.data["salesperson"])
        request.data["salesperson"] = user.salesperson.id    
            
        response = super().update(request, pk)

        # Handle salesperson change
        if oldsale.salesperson.id == user.salesperson.id:
            salesperson = Salesperson.objects.get(id = user.salesperson.id)
            salesperson.total_individual_sales += (response.data["total"] - oldsale.total)
            salesperson.total_individual_commission += (response.data["commission_perc"] - oldsale.commission_perc)
            salesperson.save()
            # Update Connected Salesperson Group Commission
            UpdateDirectCommission(salesperson, 0)
            UpdateGroupCommissions(salesperson)
            UpdateGroupCommissionsBasic(salesperson, response.data["total"] - oldsale.total)
        else:
            oldsalesperson = Salesperson.objects.get(id= oldsale.salesperson.id)
            oldsalesperson.total_individual_sales -=  oldsale.total
            oldsalesperson.total_individual_commission -= oldsale.commission_perc
            oldsalesperson.save()

            salesperson = Salesperson.objects.get(id = user.salesperson.id)
            salesperson.total_individual_sales += response.data["total"]
            salesperson.total_individual_commission += response.data["commission_perc"]
            salesperson.save()

            UpdateDirectCommission(oldsalesperson, 0)
            UpdateDirectCommission(salesperson, 0)
            UpdateGroupCommissions(oldsalesperson)
            UpdateGroupCommissions(salesperson)
            UpdateGroupCommissionsBasic(oldsalesperson, -oldsale.total)
            UpdateGroupCommissionsBasic(salesperson, response.data["total"])
            # Update both the old an new salesperson Group Commission
            # Handle this separatly when getting the total Group Sales
            # Possibly do a recalc for the oldsalesperson
        response.data["salesperson"] = user.salesperson.id
        return response

    @transaction.atomic
    def destroy(self, request, pk):
        oldsale = Sales.objects.get(id = pk)

        salesperson = Salesperson.objects.get(id= oldsale.salesperson.id)
        salesperson.total_individual_sales -= oldsale.total
        salesperson.total_individual_commission -= oldsale.commission_perc
        salesperson.save()
        UpdateDirectCommission(salesperson, 0)
        UpdateGroupCommissions(salesperson)
        UpdateGroupCommissionsBasic(salesperson, -oldsale.total )
        response = super().destroy(request, pk)
        return response

# Method to calculate all related commissions when a salesperson is given
def UpdateDirectCommission(salesperson, leval):
    if salesperson:
        salesperson.total_direct_commission = salesperson.total_individual_commission
        if salesperson.total_individual_sales > 0 :        
            salespersons = Salesperson.objects.filter(sponser=salesperson)
            total = salespersons.aggregate(Sum('total_individual_commission'))
            if total['total_individual_commission__sum'] is not None:
                salesperson.total_direct_commission += (total['total_individual_commission__sum'] * 0.1)
        else:
            salespersons = Salesperson.objects.filter(sponser=salesperson)
            total = salespersons.aggregate(Sum('total_individual_commission'))
            if total['total_individual_commission__sum'] is not None:
                salesperson.total_direct_commission += (total['total_individual_commission__sum'] * 0.05)

        salesperson.save()

        if salesperson.sponser is not None or leval < 1:
            return UpdateDirectCommission(salesperson.sponser, leval + 1)
        else:
            return

def UpdateGroupCommissions(salesperson, child_group_commission=None):
    # Refererance
    # Calculate total commission of the sponsered salesperson
    group_commission = salesperson.total_individual_commission
    group_commission += GetSponseredCommissions(salesperson, 0)
    temp_commission = GetCommission(group_commission)
    salesperson.total_group_commissions = temp_commission["commission"]
    salesperson.qualification = temp_commission["qualification"]
    # update the qualification here as well
    if child_group_commission:
        salesperson.total_group_commissions -= child_group_commission
    salesperson.save()

    if salesperson.sponser is not None:
        return UpdateGroupCommissions(salesperson.sponser, salesperson.total_group_commissions)
    else:
        return

def GetSponseredCommissions(salesperson, total):
    salespersons = Salesperson.objects.filter(sponser=salesperson)
    temp_total = total
    for person in salespersons:
        temp_total += GetSponseredCommissions(person, total + person.total_individual_commission)
    return temp_total

def UpdateGroupCommissionsBasic(salesperson, sale):
    salesperson.total_group_sales += sale
    salesperson.save()
    if salesperson.sponser is not None:
        return UpdateGroupCommissionsBasic(salesperson.sponser, sale)
    else:
        return

def GetCommission(commission_amt):
    #  1% 25,000
    #  2% 60,000
    #  3% 130,000
    #  4% 290,000
    #  5% 700,000
    if commission_amt >= 700000:
        return {"qualification": 5, "commission": commission_amt * 0.05}
    elif commission_amt >= 290000:
        return {"qualification": 4, "commission": commission_amt * 0.04}
    elif commission_amt >= 130000:
        return {"qualification": 3, "commission": commission_amt * 0.03}
    elif commission_amt >= 60000:
        return {"qualification": 2, "commission": commission_amt * 0.02}
    elif commission_amt >= 25000:
        return {"qualification": 1, "commission": commission_amt * 0.01}
    else:
        return {"qualification": 0, "commission": commission_amt * 0}