from django.db.models import Max, Q
from django.utils.timesince import timesince
from app.models import Customer
from datetime import datetime

def get_customers(params):
    qs = Customer.objects.all()
    name = params.get('name')
    if name:
        qs = qs.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

    after = params.get('birthday_after')
    before = params.get('birthday_before')
    if after:
        qs = qs.filter(birth_date__gte=datetime.fromisoformat(after).date())
    if before:
        qs = qs.filter(birth_date__lte=datetime.fromisoformat(before).date())

    qs = qs.annotate(
        last_date=Max('interactions__timestamp'),
        last_type=Max('interactions__type')
    )
    order = params.get('ordering')
    if order in ['first_name', 'company__name', 'birth_date', 'last_date']:
        qs = qs.order_by(order)
    data = []
    for c in qs:
        data.append({
            'name': f"{c.first_name} {c.last_name}",
            'company': c.company.name,
            'birthday': c.birth_date.strftime('%B %d'),
            'last': f"{timesince(c.last_date)} ago ({c.last_type})" if c.last_date else 'N/A'
        })
    return data