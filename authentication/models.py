from django.db import models

class Role(models.Model):
    role = models.CharField(max_length=10, blank=False, null=False)


class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, blank=False, null=False)
    role = models.OneToOneField(Role, on_delete=models.CASCADE, blank=False, null=False)