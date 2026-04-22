import random
from django.core.management.base import BaseCommand
from posts.models import User, Post, Like
from django.db.models import F

class Command(BaseCommand):
    help = 'Populate the database with fake likes'

    def handle(self, *args, **options):
        users = list(User.objects.all())
        posts = Post.objects.all()
        
        for post in posts:
            random_users = random.sample(users, k=random.randint(1, min(len(users), 50)))
            for user in random_users:
                like, created = Like.objects.get_or_create(user=user, post=post)
                if created:
                    Post.objects.filter(id=post.id).update(like_count=F('like_count') + 1)
              
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake likes'))
