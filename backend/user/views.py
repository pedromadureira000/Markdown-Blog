from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from settings.response_templates import error_response, unknown_exception_response, not_found_response, protected_error_response, serializer_invalid_response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout
from rest_framework import status, permissions
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from .serializers import SwaggerLoginSerializer, SwaggerProfilePasswordSerializer, UserSerializer
#  from django.db.models import Q
#  from django.db.models.deletion import ProtectedError

class CheckAuthenticated(APIView):
    @swagger_auto_schema(method='get', responses={200: UserSerializer}) 
    @action(detail=False, methods=['get'])
    def get(self, request):
        if request.user.is_authenticated:
            data = UserSerializer(request.user).data
            return Response(data)
        else:
            return error_response(detail=_("You are not authenticated."), status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        return Response(_("The CSRF cookie was sent"))

class Login(APIView):
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema(request_body=SwaggerLoginSerializer, method='post', responses={200: UserSerializer}) 
    @action(detail=False, methods=['post'])
    def post(self, request):
        if request.user.is_authenticated:
            return Response(_("User is already authenticated"))
        serializer = SwaggerLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"], request=request)
            if user is not None:
                login(request, user)
                return Response(UserSerializer(user).data)
            else:
                return error_response(detail=_("The login failed"), status=status.HTTP_401_UNAUTHORIZED)
        return serializer_invalid_response(serializer.errors)

class Logout(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            logout(request)
            return Response(_('Logged out'))
        except Exception as error:
            #  print(error)
            unknown_exception_response(action=_('log out'))

class OwnProfileView(APIView):
    @swagger_auto_schema(method='get', responses={200: UserSerializer}) 
    @action(detail=False, methods=['get'])
    def get(self, request):
        try:
            data = UserSerializer(request.user).data
            return Response(data)
        except Exception as error:
            #  print(error)
            return unknown_exception_response(action=_('get request user profile'))

    #  @swagger_auto_schema(request_body=UserSerializer) 
    #  @transaction.atomic
    #  def put(self, request):
        #  serializer = UserSerializer(request.user, data=request.data, partial=True, context={"request": request,
            #  "view": "update own profile"})
        #  if serializer.is_valid():
            #  try:
                #  serializer.save()
                #  return Response(serializer.data)
            #  except Exception as error:
                #  print(error)
                #  return unknown_exception_response(action=_('update request user profile'))
        #  return serializer_invalid_response(serializer.errors)


class UpdateOwnPassword(APIView):
    @swagger_auto_schema(request_body=SwaggerProfilePasswordSerializer) 
    @transaction.atomic
    def put(self, request):
        user = request.user
        data = request.data
        if not data.get('password'):
            return error_response(detail=_("Password field not sent"), status=status.HTTP_400_BAD_REQUEST )
        if not data.get('current_password'):
            return error_response(detail=_("Current Password field not sent"), status=status.HTTP_400_BAD_REQUEST )
        if user.check_password(data.get('current_password')):
            user.set_password(data['password'])
            user.save()
            return Response(_("Password updated"))
        return error_response(detail=_("passwords don't match"), status=status.HTTP_400_BAD_REQUEST )
