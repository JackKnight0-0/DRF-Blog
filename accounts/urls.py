from django.urls import path
from rest_framework.authtoken import views
from .views import RegisterUserView, LogoutAPIView

urlpatterns = [
    path('signup/', RegisterUserView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', LogoutAPIView.as_view())
]