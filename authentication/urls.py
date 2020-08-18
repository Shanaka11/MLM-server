from django.urls import path, include
from .views import TokenObtainPairViewNew, getUser, TokenRefreshViewNew, CreateUserView, CreateAdmin, UpdateUser
from rest_framework.routers import DefaultRouter
from .api import RoleApi, UserProfileApi, DocumentApi, AdsApi

router = DefaultRouter()
router.register('role', RoleApi)
router.register('profile', UserProfileApi)
router.register('document', DocumentApi)
router.register('ads', AdsApi)

urlpatterns = [
    path('user', getUser),
    path('create/admin', CreateAdmin),
    path('create', CreateUserView.as_view()),
    path('token', TokenObtainPairViewNew.as_view()),
    path('refresh', TokenRefreshViewNew.as_view()),
    path('update', UpdateUser),
    path('', include( router.urls ))
]