from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Salesperson(models.Model):
    # Tabel Name should be SALESPERSON
    # Add user as a one to one field
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    cell = models.CharField(max_length=20, blank=False, null=False)
    sponser = models.ForeignKey('Salesperson', blank=True, null=True, on_delete=models.CASCADE)
    realestate_id = models.IntegerField(blank=True, null=True)
    # What is qualification - commission percentage 
    qualification = models.FloatField(blank=True, null=True)
    total_individual_sales = models.FloatField(blank=True, null=True, default=0)
    total_individual_commission = models.FloatField(blank=True, null=True, default=0)
    total_direct_commission = models.FloatField(blank=True, null=True, default=0)
    total_group_sales = models.FloatField(blank=True, null=True, default=0)
    total_group_commissions = models.FloatField(blank=True, null=True, default=0)

class Sales(models.Model):
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE, blank=False, null=False)
    total = models.FloatField(blank=False, null=False)
    commission_perc = models.FloatField(blank=False, null=False)

# Methods to calculate commissions