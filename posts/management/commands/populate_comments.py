from faker import Faker
from django.core.management.base import BaseCommand
from posts.models import User, Post, Like, Comment, Follow

class Command(BaseCommand):
    help = 'Populate the database with fake comments'

    def handle(self, *args, **options):
        fake = Faker()
        posts = Post.objects.all()
        for _ in range(200):
            author = fake.random_element(User.objects.all())
            post = fake.random_element(posts)
            content = fake.text(max_nb_chars=280)
            Comment.objects.create(author=author, post=post, content=content)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake comments'))