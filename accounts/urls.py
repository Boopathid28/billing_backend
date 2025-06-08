from django.urls import path
from .views import *

urlpatterns = [
    # Authentication APIs
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/<int:pk>/', ChangePasswordView.as_view()),
]