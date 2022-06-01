from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _
from .models import Menu, SubMenu, Page

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields =  ['slug', 'default_submenu', 'title', 'icon']

class UpdateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields =  ['slug', 'default_submenu', 'title', 'icon']

    def validate_default_submenu(self, value):
        if value.menu_id != self.instance.slug:
            raise serializers.ValidationError(_("You cannot choose a default submenu that belongs to another menu."))
        return value

    #  def validate_slug(self, value):
        #  return value

    def update(self, instance, validated_data):
        slug = instance.slug
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if validated_data.get('slug'):
            # When I save the instance it will create another instance instead of updating the pk field.
            # Then I have to delete the previous one.
            Menu.objects.get(slug=slug).delete() 
        return instance

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields =  ['submenu_id', 'slug', 'menu', 'title', 'icon']
        read_only_fields = ['submenu_id']
        validators = [UniqueTogetherValidator(queryset=SubMenu.objects.all(), fields=['slug', 'menu'], 
            message=_("The slug field must be unique by menu."))]

    #  def validate(self, attrs):
            #  raise NotFound(detail={"error": [_("Item table not found.")]})
        #  return super().validate(attrs)

    def create(self, validated_data):
        validated_data['submenu_id'] = validated_data['menu'].slug + "*" + validated_data['slug']
        return super().create(validated_data)

class UpdateSubMenuSerializer(serializers.ModelSerializer):
    #  menu_id=serializers.HiddenField(default=UserContracting())
    class Meta:
        model = SubMenu
        validators = [UniqueTogetherValidator(queryset=SubMenu.objects.all(), fields=['slug', 'menu'], 
            message=_("The slug field must be unique by menu."))]
        fields =  ['slug', 'menu', 'title', 'icon']
        read_only_fields =  ['menu', 'submenu_id']

    #  def validate(self, attrs):
        #  if attrs.get('slug'):
            #  pass
        #  return super().validate(attrs)

    def update(self, instance, validated_data):
        submenu_id = instance.submenu_id
        for attr, value in validated_data.items():
            if attr == 'slug':
                setattr(instance, 'submenu_id', instance.menu_id + "*" + value)
            setattr(instance, attr, value)
        instance.save()
        if validated_data.get('slug'):
            SubMenu.objects.get(submenu_id=submenu_id).delete() 
        return instance

class PageSerializer(serializers.ModelSerializer):
    #  item_table = serializers.SlugRelatedField(slug_field='item_table_compound_id', queryset=ItemTable.objects.all())
    class Meta:
        model = Page
        fields =  ['page_id','slug', 'submenu', 'title', 'description', 'image', 'markdown_text']
        read_only_fields = ['page_id']
        validators = [UniqueTogetherValidator(queryset=Page.objects.all(), fields=['slug', 'submenu'], 
            message=_("The slug field must be unique by submenu."))]

    def create(self, validated_data):
        validated_data['page_id'] = validated_data['submenu'].submenu_id + "*" + validated_data['slug']
        return super().create(validated_data)

class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        validators = [UniqueTogetherValidator(queryset=Page.objects.all(), fields=['slug', 'submenu'],
            message=_("The slug field must be unique by submenu."))]
        fields =  ['page_id', 'slug', 'submenu', 'title', 'description', 'image', 'markdown_text']
        read_only_fields =  ['page_id', 'submenu']

    def update(self, instance, validated_data):
        page_id = instance.page_id
        for attr, value in validated_data.items():
            if attr == 'slug':
                setattr(instance, 'page_id', instance.submenu_id + "*" + value)
            setattr(instance, attr, value)
        instance.save()
        if validated_data.get('slug'):
            Page.objects.get(page_id=page_id).delete() 
        return instance
