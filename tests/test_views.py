import pytest
from posts.models import User, Post, Profile, Comment, Like, Follow

pytestmark = pytest.mark.django_db

@pytest.fixture
def user():
  return User.objects.create_user(username="test_user_one", email="test_email_one@example.com", display_name="test_user_one", password="password123")

@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client

class TestProfileViewSet:
  def test_get_profile(self, authenticated_client, user):
    _ = Profile.objects.create(user=user)
    response = authenticated_client.get('/profiles/')
    assert response.status_code == 200
    assert len(response.data) > 0
    
  def test_get_profile_by_id(self, authenticated_client, user):
    profile = Profile.objects.create(user=user)
    response = authenticated_client.get(f'/profiles/{profile.id}/')
    assert response.status_code == 200
    assert response.data['id'] == str(profile.id)
    
  def test_get_profile_me(self, authenticated_client, user):
    _ = Profile.objects.create(user=user)
    response = authenticated_client.get('/profiles/me/')
    assert response.status_code == 200
    assert response.data['user'] == user.id
    
  def test_get_profile_by_username(self, authenticated_client, user):
    _ = Profile.objects.create(user=user)
    response = authenticated_client.get(f'/profiles/{user.username}/')
    assert response.status_code == 200
    assert response.data['user'] == user.id
    
  

class TestUserViewSet:
  def test_get_users(self, authenticated_client, user):
    response = authenticated_client.get('/users/')
    assert response.status_code == 200
    assert len(response.data) > 0
    
  def test_follow_user(self, authenticated_client, user):
    user_to_follow = User.objects.create_user(username="test_user_two", email="test_email_two@example.com", display_name="test_user_two", password="password123")
    response = authenticated_client.post(f'/users/{user_to_follow.id}/follow/')
    assert response.status_code == 200
    assert response.data['status'] == 'user followed'
    
  def test_unfollow_user(self, authenticated_client, user):
    user_to_unfollow = User.objects.create_user(username="test_user_two", email="test_email_two@example.com", display_name="test_user_two", password="password123")
    _ = Follow.objects.create(follower=user, following=user_to_unfollow)
    response = authenticated_client.post(f'/users/{user_to_unfollow.id}/unfollow/')
    assert response.status_code == 405
    
    
  def test_get_user_posts(self, authenticated_client, user):
    _ = Post.objects.create(author=user, content="test_content")
    response = authenticated_client.get(f'/users/{user.id}/posts/')
    assert response.status_code == 200
    assert len(response.data) > 0
    
  def test_get_user_profile(self, authenticated_client, user):
    _ = Profile.objects.create(user=user)
    response = authenticated_client.get(f'/users/{user.id}/profile/')
    assert response.status_code == 200
    
  def test_get_user_suggestions(self, authenticated_client, user):
    _ = User.objects.create_user(username="test_user_two", email="test_email_two@example.com", display_name="test_user_two", password="password123")
    _ = User.objects.create_user(username="test_user_three", email="test_email_three@example.com", display_name="test_user_three", password="password123")
    _ = User.objects.create_user(username="test_user_four", email="test_email_four@example.com", display_name="test_user_four", password="password123")
    response = authenticated_client.get(f'/users/suggestions/')
    assert response.status_code == 200
    assert len(response.data) == 3
    
  def test_get_user_suggestions_with_less(self, authenticated_client, user):
    _ = User.objects.create_user(username="test_user_two", email="test_email_two@example.com", display_name="test_user_two", password="password123")
    _ = User.objects.create_user(username="test_user_three", email="test_email_three@example.com", display_name="test_user_three", password="password123")
    response = authenticated_client.get(f'/users/suggestions/')
    assert response.status_code == 200
    assert len(response.data) == 2

class TestPostViewSet:
  def test_get_posts(self, authenticated_client, user):
    _ = Post.objects.create(author=user, content="test_content")
    response = authenticated_client.get('/posts/')
    assert response.status_code == 200
    assert len(response.data) > 0
    
  def test_like_post(self, authenticated_client, user):
    post = Post.objects.create(author=user, content="test_content")
    response = authenticated_client.post(f'/posts/{post.id}/like/')
    assert response.status_code == 200 or response.status_code == 405
    assert response.data['status'] == 'post liked'
    
  def test_get_post_details(self, authenticated_client, user):
    post = Post.objects.create(author=user, content="test_content")
    response = authenticated_client.get(f'/posts/{post.id}/')
    assert response.status_code == 200
    assert response.data['id'] == str(post.id)
    
  def test_get_feed(self, authenticated_client, user):
    _ = Post.objects.create(author=user, content="test_content")
    user_to_follow = User.objects.create_user(username="test_user_two", email="test_email_two@example.com", display_name="test_user_two", password="password123")
    _ = Follow.objects.create(follower=user, following=user_to_follow)
    response = authenticated_client.get('/posts/feed/')
    assert response.status_code == 200
    assert len(response.data) > 0

class TestCommentViewSet:
  def test_get_comments(self, authenticated_client, user):
    post = Post.objects.create(author=user, content="test_content")
    _ = Comment.objects.create(post=post, author=user, content="test_comment")
    response = authenticated_client.get('/comments/')
    assert response.status_code == 200
    assert len(response.data) > 0

class TestLikeViewSet:
  def test_get_likes(self, authenticated_client, user):
    post = Post.objects.create(author=user, content="test_content")
    _ = Like.objects.create(post=post, user=user)
    response = authenticated_client.get('/likes/')
    assert response.status_code == 200
    assert len(response.data) > 0

class TestFollowViewSet:
  def test_get_follows(self, authenticated_client, user):
    _ = Follow.objects.create(follower=user, following=user)
    response = authenticated_client.get('/follows/')
    assert response.status_code == 200
    assert len(response.data) > 0