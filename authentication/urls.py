from django.urls import path
from .views import TokenObtainPairViewNew, getUser, TokenRefreshViewNew

urlpatterns = [
    path('user', getUser),
    # path('user/create', CreateUserView.as_view()),
    path('token', TokenObtainPairViewNew.as_view()),
    path('refresh', TokenRefreshViewNew.as_view())
]