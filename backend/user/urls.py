from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user.views import CheckAuthenticated, Logout

urlpatterns = [
    path('gettoken', obtain_auth_token, name='gettoken'),
    path('logout', Logout.as_view()),
    path('check_authenticated', CheckAuthenticated.as_view()),
]
