from rest_framework import serializers
from typing import OrderedDict
from django.utils.timezone import now
from core.models import User
from rolepermissions.roles import get_user_roles
from rolepermissions.permissions import available_perm_status
from core.validators import OnlyLettersNumbersDashAndUnderscoreUsernameValidator
from rolepermissions.roles import assign_role, clear_roles
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.permissions import grant_permission

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField() 
    role =  serializers.ChoiceField(["guest", "member"], write_only=True)
    email = serializers.EmailField()
    username = serializers.CharField(validators=[OnlyLettersNumbersDashAndUnderscoreUsernameValidator])

    class Meta:
        ref_name = "User Serializer" # fixes name collision with djoser when fetching urls with swagger
        model = User
        fields = ['username', 'email', 'password', 'roles', 'permissions', 'role']
        read_only_fields = ['roles', 'permissions']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'write_only': True},
        }

    def validate(self, attrs):
        # ---/ Role
        request_user = self.context.get("request_user")
        role = attrs.get("role")
        create_user_permission = "create_" + role
        if not has_permission(request_user, create_user_permission):
            raise serializers.ValidationError(f"You can't assign '{role}' role to an user.")

        return attrs

    def create(self, validated_data):  
        #  print('========================> : INSIDE CREATE' )
        username = validated_data['username']
        user = User(
            username=username,
            email=validated_data['email']
        )
        password = validated_data['password']
        user.set_password(password)
        user.save()
        role = validated_data["role"]
        assign_role(user, role)
        return user  # this need to be returned

    def update(self, instance, validated_data):
        clear_roles(instance)
        assign_role(instance, validated_data["role"])
        #  instance.save()
        return instance

    def get_roles(self, user):
        if isinstance(user, OrderedDict):
            roles = []
            return roles

        roles = []
        user_roles = get_user_roles(user) 
        for role in user_roles:
            roles.append(role.get_name())
        return roles

    def get_permissions(self, user):
        if isinstance(user, OrderedDict):
            permissions_list = []
            return permissions_list 

        permissions = available_perm_status(user)
        permissions_list = []

        for key, value in permissions.items():
            if value == True:
                permissions_list.append(key) 
        return permissions_list 


#--------------/Swagger

class SwaggerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
 

class SwaggerProfilePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True)
 

