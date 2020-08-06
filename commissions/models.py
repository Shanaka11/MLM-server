from django.db import models

# Create your models here.
class Salesperson(models.Model):
    # Tabel Name should be SALESPERSON
    # Add user as a one to one field
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    cell = models.CharField(max_length=20, blank=False, null=False)
    sponser = models.ManyToManyField('Salesperson', blank=True)
    # sponser_id Is this another salesperson ?
    # realestate_id - What is this
    # What is qualification - commission percentage 
    # Total commissions
    # Total group commissions
    # Have seriaizer method fields to fetch these values
    # Total individual sales
    # Total group sales 

class Sales(models.Model):
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE, blank=False, null=False)
    total = models.FloatField(blank=False, null=False)
    commission_perc = models.FloatField(blank=False, null=False)

# Methods to calculate commissions