from django.shortcuts import render
from app.controllers.customer import get_customers

def customers(request):
    data = get_customers(request.GET)
    return render(request, 'app/customer.html', {
        'customers': data,
        'filter_params': request.GET
    })