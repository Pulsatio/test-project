from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from app.models import User, Company, Customer, Interaction

class Command(BaseCommand):
    def handle(self, *args, **opts):
        fake = Faker()
        reps = [User.objects.create_user(f"rep{i+1}", password="pass") for i in range(3)]
        companies = [Company.objects.create(name=fake.company()) for _ in range(10)]
        for _ in range(1000):
            c = Customer.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(),
                birth_date=fake.date_of_birth(), company=random.choice(companies),
                representative=random.choice(reps)
            )
            for _ in range(500):
                Interaction.objects.create(
                    customer=c, type=random.choice([t[0] for t in Interaction.TYPES]),
                    timestamp=fake.date_time_between("-1y", "now", tzinfo=timezone.get_current_timezone())
                )