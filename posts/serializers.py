from os import read

from rest_framework import serializers
from .models import User, Post, Like, Comment, Follow, Profile

class UserSerializer(serializers.ModelSerializer):
    
    def get_user_posts(self, obj):
        return obj.posts.values()
    
    user_posts = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', "display_name", "is_admin", "user_posts"]
        
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
    def create(self, validated_date):
      user = User.objects.create_user(**validated_date)
      return user

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data
    
    comments = serializers.SerializerMethodField(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_display_name = serializers.CharField(source='author.display_name', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'author_display_name',  'content', 'created_at', 'like_count', "comments"]
        

class ProfileSerializer(serializers.ModelSerializer):
    def get_follower_count(self, obj):
        return obj.user.followers.count()

    def get_following_count(self, obj):
        return obj.user.following.count()
    
    user_posts = PostSerializer(many=True, source='user.posts', read_only=True)
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', "user_posts", "follower_count", "following_count"]
    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']