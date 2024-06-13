from django.contrib import admin
from django.urls import path
from visitor.views import home, login_view, logout_view

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]