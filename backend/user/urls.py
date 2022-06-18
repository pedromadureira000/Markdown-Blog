from django.urls import path
from user.views import CheckAuthenticated, GetCSRFToken, Login, Logout, OwnProfileView, UpdateOwnPassword

urlpatterns = [
    #Auth
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    path('getcsrf', GetCSRFToken.as_view()),
    path('check_authenticated', CheckAuthenticated.as_view()),
    path('own_profile', OwnProfileView.as_view()),
    path('update_own_password', UpdateOwnPassword.as_view()),
]
