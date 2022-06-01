from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from settings.response_templates import error_response, unknown_exception_response, not_found_response, protected_error_response, serializer_invalid_response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout
from rest_framework import status, permissions
#  from user.models import User
#  from drf_yasg.utils import swagger_auto_schema
#  from django.db.models import Q
#  from django.db.models.deletion import ProtectedError

class CheckAuthenticated(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        if request.user.is_authenticated:
            return Response(_("You are authenticated."))
        else:
            return error_response(detail=_("You are not authenticated."), status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            logout(request)
            return Response(_('Logged out'))
        except Exception as error:
            #  print(error)
            unknown_exception_response(action=_('log out'))
