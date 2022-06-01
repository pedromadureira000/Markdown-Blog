from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from settings.response_templates import serializer_invalid_response, unknown_exception_response, not_found_response, protected_error_response
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.db.models.deletion import ProtectedError

