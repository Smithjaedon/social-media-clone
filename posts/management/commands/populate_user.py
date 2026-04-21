from faker import Faker
from django.core.management.base import BaseCommand
from posts.models import User

class Command(BaseCommand):
    help = 'Populate the database with fake users'

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(100):
            username = fake.unique.user_name()
            email = fake.unique.email()
            display_name = fake.unique.name()
            password = 'password123'
            User.objects.create_user(username=username, email=email, display_name=display_name, password=password)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake users'))