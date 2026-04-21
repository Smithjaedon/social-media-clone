from faker import Faker
from django.core.management.base import BaseCommand
from posts.models import User, Post, Like, Comment, Follow

class Command(BaseCommand):
    help = 'Populate the database with fake posts'

    def handle(self, *args, **options):
        fake = Faker()
        users = User.objects.all()
        for _ in range(200):
            author = fake.unique.random_element(users)
            content = fake.unique.text(max_nb_chars=280)
            Post.objects.create(author=author, content=content)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake posts'))