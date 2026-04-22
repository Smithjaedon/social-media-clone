from faker import Faker
from django.core.management.base import BaseCommand
from posts.models import User, Post, Like, Comment, Follow, Profile

class Command(BaseCommand):
    help = 'Populate the database with profiles for existing users'

    def handle(self, *args, **options):
        fake = Faker()
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'profile'):
                bio = fake.text(max_nb_chars=160)
                Profile.objects.create(user=user, bio=bio)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with profiles for existing users'))