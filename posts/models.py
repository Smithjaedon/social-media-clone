from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):
  operations = [
    TrigramExtension(),
  ]

# Create your models here.
class User(AbstractUser):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  display_name = models.CharField(max_length=255, null=False)
  is_admin = models.BooleanField(default=False)
  
  class Meta:
    indexes = [
      GinIndex(fields=['display_name'], name='display_name_gin_idx'),
    ]
  
  def __str__(self):
    return self.username
  
class Profile(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True)
  
  def __str__(self):
    return f"{self.user.username}'s Profile"
  
class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  like_count = models.PositiveIntegerField(default=0, db_index=True)
  
  
  class Meta:
    indexes = [
      GinIndex(fields=['content'], name='content_gin_idx'),
    ]
  
  def __str__(self):
    return f"Post by {self.author.username} at {self.created_at}"
  
class Like(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together = ('user', 'post')
  
  def __str__(self):
    return f"{self.user.username} liked post {self.post.id}"
  
class Comment(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"Comment by {self.author.username} on post {self.post.id}"
  
  
class Follow(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together = ('follower', 'following')
  
  def __str__(self):
    return f"{self.follower.username} follows {self.following.username}"
