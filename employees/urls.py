# employees/urls.py
from django.urls import path
from .views import EmployeeLookupView, employee_search_api

app_name = 'employees'

urlpatterns = [
    path('', EmployeeLookupView.as_view(), name='lookup'),
    path('api/search/', employee_search_api, name='search_api'),
]