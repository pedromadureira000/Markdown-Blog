from django.urls import path
from user.views import CheckAuthenticated, GetCSRFToken, Login, Logout, UpdateOwnPassword

urlpatterns = [
    #Auth
    path('login', Login.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),
    path('getcsrf', GetCSRFToken.as_view(), name="get_csrf_token"),
    path('check_authenticated', CheckAuthenticated.as_view(), name="check_authenticated"),
    path('update_own_password', UpdateOwnPassword.as_view(), name="update_own_password"),
]
