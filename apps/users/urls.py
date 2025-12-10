from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import (
    RegisterUserView,
    LoginUserView,
    LogoutUserView,
    HealthCheckView,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('health/', HealthCheckView.as_view(), name='health'),
]