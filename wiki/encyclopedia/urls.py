from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"), #i added
    path("wiki/encyclopedia/search", views.search, name="search"),   #i added
    path("randompage/", views.randompage, name="randompage"),   #i added
    path("wiki/encyclopedia/newPage", views.newPage, name="newPage"),   #i added
    path('saveEntry/', views.saveEntry, name='saveEntry'),
    path("wiki/encyclopedia/editPage", views.editButton, name="editButton"),   #i added
    path('saveEntry2/', views.saveEntry2, name='saveEntry2'),


]
