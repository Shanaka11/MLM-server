from django.urls import path
from .views import TokenObtainPairViewNew

urlpatterns = [
    # path('user/current_user/', get_current_user),
    # path('user/create', CreateUserView.as_view()),
    path('token', TokenObtainPairViewNew.as_view())
    # path('user/refresh/', TokenRefreshViewNew.as_view())
]