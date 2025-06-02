# core/urls.py
from django.urls import path
from .views import dashboard_view

app_name = 'core'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]