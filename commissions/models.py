from django.db import models

# Create your models here.
class Salesperson(models.Model):
    # Tabel Name should be SALESPERSON
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    cell = models.CharField(max_length=20, blank=False, null=False)
    # sponser_id Is this another salesperson ?
    # realestate_id - What is this

class Sales(models.Model):
    salesperosn = models.ForeignKey(Salesperson, on_delete=models.CASCADE, blank=False, null=False)
    total = models.FloatField(blank=False, null=False)
    commission_perc = models.FloatField(blank=False, null=False)
