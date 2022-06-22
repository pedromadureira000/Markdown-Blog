from django.urls import path

from core.views import GetMenus, MenuView, MenuWithSubmenusWithPages, PageView, SpecificMenu, SpecificPage, SpecificSubMenu, SubMenuView, fetchPageToBuildBlog, fetchPagesToBuildBlog, fetchSubmenusToBuildBlog

app_name = 'core'
urlpatterns = [
    path('menu', MenuView.as_view()),
    path('get_menus', GetMenus.as_view()),
    path('menu/<int:id>', SpecificMenu.as_view()),
    path('submenu', SubMenuView.as_view()),
    path('submenu/<int:id>', SpecificSubMenu.as_view()),
    path('page', PageView.as_view()),
    path('page/<int:id>', SpecificPage.as_view()),
    # Blog APIS
    path('get_menus_submenus_and_pages', MenuWithSubmenusWithPages.as_view()),
    path('fetch_submenus_to_build_blog/<str:menu_slug>', fetchSubmenusToBuildBlog.as_view()),
    path('fetch_pages_to_build_blog/<str:menu_slug>/<str:submenu_slug>', fetchPagesToBuildBlog.as_view()),
    path('fetch_page_to_build_blog/<str:menu_slug>/<str:submenu_slug>/<str:page_slug>', fetchPageToBuildBlog.as_view()),
    
]
