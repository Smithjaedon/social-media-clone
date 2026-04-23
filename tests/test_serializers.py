import pytest
from posts.serializers import UserSerializer, ProfileSerializer, PostSerializer, LikeSerializer, CommentSerializer, FollowSerializer
from posts.models import User, Profile, Post, Like, Comment, Follow

pytestmark = pytest.mark.django_db

class TestUserSerializer:
  def test_valid_data(self):
    data = {
      "username": "test_user",
      "email": "test_email@example.com",
      "display_name": "test_user",
      "password": "password123"
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    
  def test_missing_field(self):
    data = {
      "username": "test_user",
      "display_name": "test_user",
      "email": "test_email@example.com",
    }
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors
    
    
class TestProfileSerializer:
  def test_valid_data(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    data = {
      "user": user.id,
      "bio": "test_bio"
    }
    serializer = ProfileSerializer(data=data)
    assert serializer.is_valid()
    
  def test_missing_field(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    data = {
      "bio": ""
    }
    serializer = ProfileSerializer(data=data)
    assert not serializer.is_valid()
    assert "user" in serializer.errors
    
class TestProfileSerializer:
  def test_valid_data(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    data = {
      "user": user.id,
      "bio": "test_bio"
    }
    serializer = ProfileSerializer(data=data)
    assert serializer.is_valid()
    
  def test_missing_field(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    data = {
      "bio": ""
    }
    serializer = ProfileSerializer(data=data)
    assert not serializer.is_valid()
    assert "user" in serializer.errors
    
    
class TestLikeSerializer:
  def test_valid_data(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    post = Post.objects.create(author=user, content="test_content")
    data = {
      "user": user.id,
      "post": post.id
    }
    serializer = LikeSerializer(data=data)
    assert serializer.is_valid()
    
  def test_missing_field(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    data = {
      "user": user.id
    }
    serializer = LikeSerializer(data=data)
    assert not serializer.is_valid()
    assert "post" in serializer.errors
    
    
class TestFollowSerializer:
  def test_valid_data(self):
    user = User.objects.create_user(username="test_user1", email="test_email@example.com", display_name="test_user2", password="password123")
    another_user = User.objects.create_user(username="test_user2", email="test_email@example.com", display_name="test_user2", password="password123")
    data = {
      "follower": user.id,
      "following": another_user.id
    }
    serializer = FollowSerializer(data=data)
    assert serializer.is_valid()
    
  def test_missing_field(self):
    user = User.objects.create_user(username="test_user1", email="test_email@example.com", display_name="test_user1", password="password123")
    another_user = User.objects.create_user(username="test_user2", email="test_email@example.com", display_name="test_user2", password="password123")
    data = {
      "follower": user.id,
    }
    serializer = FollowSerializer(data=data)
    assert not serializer.is_valid()
    assert "following" in serializer.errors
    
    
class TestPostSerializers:
  def test_valid_data(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    data = {
      "author": user.id,
      "content": "test_content"
    }
    serializer = PostSerializer(data=data)
    assert serializer.is_valid()
  def test_missing_field(self):
    user = User.objects.create_user(username="test_user", email="test_email@example.com", display_name="test_user", password="password123")
    data = {
      "content": "test_content"
    }
    serializer = PostSerializer(data=data)
    assert not serializer.is_valid()
    assert "author" in serializer.errors
