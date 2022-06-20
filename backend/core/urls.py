from django.urls import path

from core.views import MenuView, PageView, SpecificMenu, SpecificPage, SpecificSubMenu, SubMenuView

app_name = 'core'
urlpatterns = [
    path('menu', MenuView.as_view()),
    path('menu/<int:id>', SpecificMenu.as_view()),
    path('submenu', SubMenuView.as_view()),
    path('submenu/<int:id>', SpecificSubMenu.as_view()),
    path('page', PageView.as_view()),
    path('page/<int:id>', SpecificPage.as_view()),
]
