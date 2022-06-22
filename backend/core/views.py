from django.db import transaction
from django.db.models.deletion import ProtectedError
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from core.serializers import MenuSerializer, MenuWithSubmenusWithPagesSerializer, PageSerializer, SubMenuSerializer, UpdateMenuSerializer, UpdatePageSerializer, UpdateSubMenuSerializer
from settings.response_templates import serializer_invalid_response, unknown_exception_response
from .models import Menu, SubMenu, Page
from rest_framework.decorators import action
from django.db.models import Prefetch


class MenuView(APIView):
    @swagger_auto_schema(request_body=MenuSerializer) 
    @transaction.atomic
    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except Exception:
                transaction.rollback()
                return unknown_exception_response(action=_('create menu'))
        return serializer_invalid_response(serializer.errors)


class SpecificMenu(APIView):
    @transaction.atomic
    @swagger_auto_schema(request_body=UpdateMenuSerializer) 
    def put(self, request, id):
        try:
            menu = Menu.objects.get(id=id)
        except Menu.DoesNotExist:
            return Response({"error":[_("The menu was not found.")]}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateMenuSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(_("The menu was updated."))
            except Exception:
                transaction.rollback()
                return unknown_exception_response(action=_('update menu'))
        return serializer_invalid_response(serializer.errors)
    @transaction.atomic
    def delete(self, request, id):
        try:
            menu = Menu.objects.get(id=id)
        except Menu.DoesNotExist:
            return Response({"error":[_("The menu was not found.")]}, status=status.HTTP_404_NOT_FOUND)
        try:
            menu.delete()
            return Response(_('The menu was deleted'))
        except ProtectedError:
            return Response({"error":[_("You cannot delete this menu because it has records linked to it.")]}, 
                    status=status.HTTP_400_BAD_REQUEST) 
        except Exception:
            transaction.rollback()
            return unknown_exception_response(action=_('delete menu'))


class SubMenuView(APIView):
    @swagger_auto_schema(request_body=SubMenuSerializer) 
    @transaction.atomic
    def post(self, request):
        serializer = SubMenuSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except Exception:
                transaction.rollback()
                return unknown_exception_response(action=_('create submenu'))
        return serializer_invalid_response(serializer.errors)

class SpecificSubMenu(APIView):
    @swagger_auto_schema(method='get', responses={200: SubMenuSerializer(many=True)}) 
    @action(detail=False, methods=['get'])
    def get(self, request, id):
        submenus = SubMenu.objects.filter(menu_id=id)
        return Response(SubMenuSerializer(submenus, many=True).data)

    @transaction.atomic
    @swagger_auto_schema(request_body=UpdateSubMenuSerializer) 
    def put(self, request, id):
        try:
            submenu = SubMenu.objects.get(id=id)
        except SubMenu.DoesNotExist:
            return Response({"error":[_("The submenu was not found.")]}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateSubMenuSerializer(submenu, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(_("The submenu was updated."))
            except Exception:
                transaction.rollback()
                return unknown_exception_response(action=_('update submenu'))
        return serializer_invalid_response(serializer.errors)

    @transaction.atomic
    def delete(self, request, id):
        try:
            submenu = SubMenu.objects.get(id=id)
        except SubMenu.DoesNotExist:
            return Response({"error":[_("The submenu was not found.")]}, status=status.HTTP_404_NOT_FOUND)
        try:
            submenu.delete()
            return Response(_('The submenu was deleted'))
        except ProtectedError:
            return Response({"error":[_("You cannot delete this submenu because it has records linked to it.")]}, 
                    status=status.HTTP_400_BAD_REQUEST) 
        except Exception:
            transaction.rollback()
            return unknown_exception_response(action=_('delete submenu'))

class PageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=PageSerializer) 
    @transaction.atomic
    def post(self, request, format=None):
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except Exception:
                transaction.rollback()
                return unknown_exception_response(action=_('create page'))
        return serializer_invalid_response(serializer.errors)

class SpecificPage(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(method='get', responses={200: PageSerializer(many=True)}) 
    @action(detail=False, methods=['get'])
    def get(self, request, id):
        pages = Page.objects.filter(submenu_id=id)  
        return Response(PageSerializer(pages, many=True).data)

    @transaction.atomic
    @swagger_auto_schema(request_body=UpdatePageSerializer) 
    def put(self, request, id):
        try:
            page = Page.objects.get(id=id)
        except Page.DoesNotExist:
            return Response({"error":[_("The page was not found.")]}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdatePageSerializer(page, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except Exception:
                transaction.rollback()
                return unknown_exception_response(action=_('update page'))
        return serializer_invalid_response(serializer.errors)
    @transaction.atomic
    def delete(self, request, id):
        try:
            page = Page.objects.get(id=id)
        except Page.DoesNotExist:
            return Response({"error":[_("The page was not found.")]}, status=status.HTTP_404_NOT_FOUND)
        try:
            page.delete()
            return Response(_('The page was deleted'))
        except ProtectedError:
            return Response({"error":[_("You cannot delete this page because it has records linked to it.")]}, 
                    status=status.HTTP_400_BAD_REQUEST) 
        except Exception:
            transaction.rollback()
            return unknown_exception_response(action=_('delete page'))

# ----------------- / Blog APIS
class GetMenus(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(method='get', responses={200: MenuSerializer(many=True)}) 
    @action(detail=False, methods=['get'])
    def get(self, request):
        menus = Menu.objects.select_related('default_submenu').all()  
        return Response(MenuSerializer(menus, many=True).data)

class MenuWithSubmenusWithPages(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(method='get', responses={200: MenuWithSubmenusWithPagesSerializer(many=True)}) 
    @action(detail=False, methods=['get'])
    def get(self, request):
        pages = Page.objects.all()
        submenus = SubMenu.objects.prefetch_related(
            Prefetch('page_set', queryset=pages, to_attr='pages')
        ).all()
        menus = Menu.objects.select_related('default_submenu').prefetch_related(
            Prefetch('submenu_set', queryset=submenus, to_attr='submenus')
        ).all()  
        return Response(MenuWithSubmenusWithPagesSerializer(menus, many=True).data)

class fetchSubmenusToBuildBlog(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(method='get', responses={200: SubMenuSerializer(many=True)}) 
    @action(detail=False, methods=['get'])
    def get(self, request, menu_slug):
        submenus = SubMenu.objects.filter(menu__slug=menu_slug)
        return Response(SubMenuSerializer(submenus, many=True).data)

class fetchPagesToBuildBlog(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(method='get', responses={200: PageSerializer(many=True)}) 
    @action(detail=False, methods=['get'])
    def get(self, request, menu_slug, submenu_slug):
        pages = Page.objects.filter(submenu__menu__slug=menu_slug, submenu__slug=submenu_slug)  
        return Response(PageSerializer(pages, many=True).data)

class fetchPageToBuildBlog(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(method='get', responses={200: PageSerializer()}) 
    @action(detail=False, methods=['get'])
    def get(self, request, menu_slug, submenu_slug, page_slug):
        try:
            page = Page.objects.get(submenu__menu__slug=menu_slug, submenu__slug=submenu_slug, slug=page_slug)
        except Page.DoesNotExist:
            return Response({"error":[_("The page was not found.")]}, status=status.HTTP_404_NOT_FOUND)
        return Response(PageSerializer(page).data)
