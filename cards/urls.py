from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.create, name='cards_make'),
    path('c/', views.see_card, name='cards_see'),
    path('socomp/', views.changecurrent, name='cards_change'),
    path('t/<str:tag>',views.tagview, name='cards_tag')
]
