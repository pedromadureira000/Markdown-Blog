from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _
from .models import Menu, SubMenu, Page

class MenuSerializer(serializers.ModelSerializer):
    class SubMenuAUXSerializer(serializers.ModelSerializer):
        class Meta:
            model = SubMenu
            fields =  ['id', 'title']

    default_submenu = SubMenuAUXSerializer(read_only=True)
    class Meta:
        model = Menu
        fields =  ['id', 'slug', 'default_submenu', 'title', 'icon']
        read_only_fields = ['default_submenu']


class UpdateMenuSerializer(serializers.ModelSerializer):
    default_submenu = serializers.PrimaryKeyRelatedField(queryset=SubMenu.objects.all(), allow_null=True)
    class Meta:
        model = Menu
        fields =  ['id', 'slug', 'default_submenu', 'title', 'icon']
        read_only_fields = ['id']

    def validate_default_submenu(self, value):
        if value: # It can be null
            if value.menu_id != self.instance.id:
                raise serializers.ValidationError(_("You cannot choose a default submenu that belongs to another menu."))
        return value

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields =  ['id', 'slug', 'menu', 'title', 'icon']
        #  read_only_fields = ['id']
        validators = [UniqueTogetherValidator(queryset=SubMenu.objects.all(), fields=['slug', 'menu'], 
            message=_("The slug field must be unique by menu."))]

    #  def validate(self, attrs):
            #  raise NotFound(detail={"error": [_("Item table not found.")]})
        #  return super().validate(attrs)

class UpdateSubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        validators = [UniqueTogetherValidator(queryset=SubMenu.objects.all(), fields=['slug', 'menu'], 
            message=_("The slug field must be unique by menu."))]
        fields =  ['slug', 'menu', 'title', 'icon']
        read_only_fields =  ['menu', 'id']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields =  ['id','slug', 'submenu', 'title', 'description', 'image', 'markdown_text']
        #  read_only_fields = ['id']
        validators = [UniqueTogetherValidator(queryset=Page.objects.all(), fields=['slug', 'submenu'], 
            message=_("The slug field must be unique by submenu."))]


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        validators = [UniqueTogetherValidator(queryset=Page.objects.all(), fields=['slug', 'submenu'],
            message=_("The slug field must be unique by submenu."))]
        fields =  ['id', 'slug', 'submenu', 'title', 'description', 'image', 'markdown_text']
        read_only_fields =  ['id', 'submenu']
