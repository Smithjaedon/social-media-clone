from rest_framework import serializers
from .models import User, Post, Like, Comment, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "display_name", "is_admin"]
        
    def create(self, validated_date):
      user = User.objects.create_user(**validated_date)
      return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'like_count']
        
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']