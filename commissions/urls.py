from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import SalesApi, SalespersonApi
from .views import getConnectedSalesperson

router = DefaultRouter()
router.register('sales', SalesApi)
router.register('salesperson', SalespersonApi)

urlpatterns = [
    path('',include( router.urls )),
    path('connected_salesperson/<int:id>', getConnectedSalesperson)
]