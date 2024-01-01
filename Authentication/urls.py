from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserSignUpView, home, complete_sign_up , key_exchange ,receive_session_key_from_client,send_projects, send_marks, send_csr

urlpatterns = [
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/sign-up/', UserSignUpView.as_view(), name='api_signup'),
    path('api/home/', home, name='home'),
    path('api/complete_sign_up/', complete_sign_up, name='complete_sign_up'),
    path('api/key_exchange/', key_exchange, name='key_exchange'),
    path('api/send_session_key_to_server/', receive_session_key_from_client, name='send_session_key_to_server'),
    path('api/send_projects/', send_projects, name='send_projects'),
    path('api/send_marks/', send_marks, name='send_marks'),
    path('api/send_csr/', send_csr, name='send_marks'),
]
