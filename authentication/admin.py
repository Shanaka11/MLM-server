from django.contrib import admin
from .models import Role, UserProfile, Document, Ads
# Register your models here.
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(Ads)