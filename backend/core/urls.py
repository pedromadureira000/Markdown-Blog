from django.urls import path

from core.views import MenuView, PageView, SpecificMenu, SpecificPage, SpecificSubMenu, SubMenuView

app_name = 'core'
urlpatterns = [
    path('menu', MenuView.as_view()),
    path('menu/<slug>', SpecificMenu.as_view()),
    path('submenu', SubMenuView.as_view()),
    path('submenu/<submenu_id>', SpecificSubMenu.as_view()), 
    path('page', PageView.as_view()),
    path('page/<page_id>', SpecificPage.as_view()), 
]
