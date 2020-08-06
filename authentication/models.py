from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    role = models.CharField(unique=True, max_length=10, blank=False, null=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, blank=False, null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=False)