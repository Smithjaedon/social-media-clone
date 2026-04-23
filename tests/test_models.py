import pytest
from posts.models import User, Profile, Post, Like, Comment, Follow

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
  return User.objects.create(username="test_user", email="test_email", display_name="test_user", is_admin=False)

def test_user_model(user):
  assert user.display_name == 'test_user'
  

def test_profile_model_bio(user):
  me_profile = Profile.objects.create(user=user, bio="test_bio")
  assert me_profile.bio == 'test_bio'
  

def test_post_model(user):
  me_post = Post.objects.create(author=user, content="test_content")
  assert me_post.content == 'test_content'
  

def test_like_model(user):
  me_post = Post.objects.create(author=user, content="test_content")
  me_like = Like.objects.create(user=user, post=me_post)
  assert me_like.post == me_post
  

def test_comment_model(user):
  me_post = Post.objects.create(author=user, content="test_content")
  me_comment = Comment.objects.create(author=user, post=me_post, content="test_content")
  assert me_comment.post == me_post
  

def test_follow_model(user):
  another_me = User.objects.create(username="another_test_user", email="another_test_email", display_name="another_test_user", is_admin=False)
  me_follow = Follow.objects.create(follower=user, following=another_me)
  assert me_follow.following == another_me