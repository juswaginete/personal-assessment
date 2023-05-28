from django.urls import path

from .views import UserSignupView, LoginAPIView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('login/', LoginAPIView.as_view(), name="login"),
]
