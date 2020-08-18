from django.contrib import admin
from .models import Role, UserProfile, Document
# Register your models here.
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Document)