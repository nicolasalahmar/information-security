from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserSignUpView, home, complete_sign_up , key_exchange ,send_session_key

urlpatterns = [
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/sign-up/', UserSignUpView.as_view(), name='api_signup'),
    path('api/home/', home, name='home'),
    path('api/complete_sign_up/', complete_sign_up, name='complete_sign_up'),
    path('api/key_exchange/', key_exchange, name='key_exchange'),
    path('api/send_session_key/', send_session_key, name='send_session_key'),
]
