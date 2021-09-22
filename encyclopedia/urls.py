from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("wiki/<str:entry>", views.entry, name='entry'),
    path("search", views.search, name='search'),
    path("create", views.create, name='create')
]