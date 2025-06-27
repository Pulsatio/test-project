from django.db.models import Q, OuterRef, Subquery
from django.utils import timezone
from django.utils.timesince import timesince
from app.models import Customer, Interaction
from datetime import datetime, timedelta

def get_customers(params):
    name = params.get('name')
    after = params.get('birthday_after')
    before = params.get('birthday_before')
    birthday_week = params.get('birthday_week') == 'on'
    interaction_type = params.get('interaction_type')
    ordering = params.get('ordering')
    
    qs = Customer.objects.select_related('company')

    if name:
        qs = qs.filter(
            Q(first_name__icontains=name) | 
            Q(last_name__icontains=name)
        )
    
    if birthday_week:
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        dates_in_week = [start_of_week + timedelta(days=i) for i in range(7)]
        
        birthday_filter = Q()
        for d in dates_in_week:
            birthday_filter |= Q(birth_date__month=d.month, birth_date__day=d.day)
        
        qs = qs.filter(birthday_filter)
    else:
        if after:
            try:
                after_date = datetime.strptime(after, '%Y-%m-%d').date()
                qs = qs.filter(birth_date__gte=after_date)
            except (ValueError, TypeError):
                pass
        if before:
            try:
                before_date = datetime.strptime(before, '%Y-%m-%d').date()
                qs = qs.filter(birth_date__lte=before_date)
            except (ValueError, TypeError):
                pass
    
    if interaction_type:
        qs = qs.filter(interactions__type=interaction_type)
    
    last_interaction_subquery = Interaction.objects.filter(
        customer=OuterRef('pk')
    ).order_by('-timestamp').values('timestamp', 'type')[:1]
    
    qs = qs.annotate(
        last_date=Subquery(last_interaction_subquery.values('timestamp')),
        last_type=Subquery(last_interaction_subquery.values('type'))
    ).distinct()
    
    order_mapping = {
        'name': 'first_name',
        'company__name': 'company__name',
        'birth_date': 'birth_date',
        'last_date': 'last_date',
        '-last_date': '-last_date'
    }
    
    order_field = order_mapping.get(ordering, 'first_name')
    qs = qs.order_by(order_field)
    
    data = []
    for c in qs:
       
        last_interaction = 'N/A'
        if c.last_date:
            
            time_diff = timesince(c.last_date, timezone.now())
            last_interaction = f"{time_diff} ago ({c.last_type})"
        
        data.append({
            'name': f"{c.first_name} {c.last_name}",
            'company': c.company.name,
            'birthday': c.birth_date.strftime('%B %d'),
            'last': last_interaction,
            'last_type': c.last_type  #
        })
    
    return data