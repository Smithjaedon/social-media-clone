from django.core.management.base import BaseCommand
from posts.models import User, Post, Like
from django.db.models import F

class Command(BaseCommand):
    help = 'Populate the database with fake likes'

    def handle(self, *args, **options):
        
        posts = Post.objects.all().order_by('?')
        for post in posts:
            for _ in range(10):
                user = User.objects.order_by('?').first()
                like, created = Like.objects.get_or_create(user=user, post=post)
                if created:
                    Post.objects.filter(id=post.id).update(like_count=F('like_count') + 1)
              
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake likes'))