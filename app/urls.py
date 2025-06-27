from django.contrib import admin
from django.urls import path
from app.views import customer

urlpatterns = [
    path('', customer.customers, name='customers'),
]