from django.urls import path, include
from .views import TokenObtainPairViewNew, getUser, TokenRefreshViewNew, CreateUserView
from rest_framework.routers import DefaultRouter
from .api import RoleApi, UserProfileApi

router = DefaultRouter()
router.register('role', RoleApi)
router.register('profile', UserProfileApi)

urlpatterns = [
    path('user', getUser),
    path('create', CreateUserView.as_view()),
    path('token', TokenObtainPairViewNew.as_view()),
    path('refresh', TokenRefreshViewNew.as_view()),
    path('', include( router.urls ))
]