from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, requires_csrf_token
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission, has_role
from core.serializers import SwaggerLoginSerializer, SwaggerProfilePasswordSerializer, UserSerializer 
#  from rest_framework.authtoken.models import Token
from core.models import User
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({"sucess": "csrf cookie set"})


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema(request_body=SwaggerLoginSerializer) 
    def post(self, request):
        if request.user.is_authenticated:
            return Response({"status": "already_authenticated."})
        username = request.data.get('username')
        password = request.data.get('password')
        if not username:
            return Response({'error': "'username' field is missing."}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': "'password' field is missing."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password, request=request)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        else:
            return Response({"status": "login_failed"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            logout(request)
            return Response({'success': 'Loggout out'})
        except Exception as error:
            print(error)
            return Response({'error': 'Something went wrong when logging out.'})


@method_decorator( ensure_csrf_cookie, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)


class CreateUserView(APIView):
    @swagger_auto_schema(request_body=UserSerializer) 
    @transaction.atomic  # if there is some error, it will be roolback all transaction
    def post(self, request):
        try:
            if has_permission(request.user, 'create_guest') or has_permission(request.user, 'create_member'):
                data = request.data
                serializer = UserSerializer(data=data, context={"request_user":request.user})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            transaction.rollback()
            print(error)
            return Response({"error": "Something get wrong when trying to create user."}, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsers(APIView):
    def get(self, request):
        user = request.user
        if has_permission(user, 'get_users'):
            users = User.objects.all().filter(is_superuser=False)
            data = UserSerializer(users, many=True).data
            return Response(data)

        return Response({'error': "You don't have permission to access this resource."},status=status.HTTP_401_UNAUTHORIZED)


class DeleteAccountView(APIView):
    @transaction.atomic  
    def delete(self, request, username, format=None):
        if has_permission(request.user, 'delete_user'):
            try: 
                user = User.objects.get(username=username)

                if user.is_superuser or has_role(user, 'admin'):
                    return Response({'error': "You don't have permission to delete this user."},status=status.HTTP_401_UNAUTHORIZED)
                user.delete()
                return Response({"success": "User deleted successfully."})
            except User.DoesNotExist:
              return Response(status=status.HTTP_404_NOT_FOUND) 

            except Exception as error:
                print(error)
                transaction.rollback()

        return Response({'error': "You don't have permission to access this resource."},status=status.HTTP_401_UNAUTHORIZED)


#  class updateUserProfile(APIView):
    #  @swagger_auto_schema(request_body=UserSerializer) 
    #  def put(self, request):
        #  user = request.user
        #  serializer = UserSerializer(user, data=request.data, partial=True) # (partial=True)we dont want to update every field
        #  if serializer.is_valid(raise_exception=True):  # ????????????????
            #  serializer.save()
            #  return Response(serializer.data)
        #  else:
            #  return Response({"status": "Bad request."},status=status.HTTP_400_BAD_REQUEST)

class UpdateUser(APIView):
    @swagger_auto_schema(request_body=UserSerializer) 
    def put(self, request):
        user = User.objects.get(username=request.data.get("username"))
        serializer = UserSerializer(user, data=request.data, partial=True, context={"request_user":request.user})
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"status": "Bad request."},status=status.HTTP_400_BAD_REQUEST)


class UpdateUserPassword(APIView):
    @swagger_auto_schema(request_body=SwaggerProfilePasswordSerializer) 
    def put(self, request):
        user = request.user
        data = request.data
        if not data.get('password'):
            return Response({"status": "Password field not sent."}, status=status.HTTP_400_BAD_REQUEST)

        if not data.get('current_password'):
            return Response({"status": "Current Password field not sent."},status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(data.get('current_password')):
            user.set_password(data['password'])
            user.save()
            return Response({"status": "Password updated"})
        return Response({"status": "passwords don't match"},status=status.HTTP_400_BAD_REQUEST)

