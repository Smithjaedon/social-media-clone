from multiprocessing import context

from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Post, Like, Comment, Follow, Profile
from .serializers import UserSerializer, PostSerializer, LikeSerializer, CommentSerializer, FollowSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import F
from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return []
        elif self.action in ['update', 'destroy']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        postId = self.request.query_params.get('postId', None)
        if search or postId:
            return self.queryset.filter(username__icontains=search, posts__id=postId)
        return self.queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='follow')
    def follow_user(self, request, pk=None):
        with transaction.atomic():
            user_to_follow = self.get_object()
            user = request.user
            if user == user_to_follow:
                return Response({'status': 'cannot follow yourself'}, status=400)
            follow, created = Follow.objects.get_or_create(follower=user, following=user_to_follow)
            if created:
                return Response({'status': 'user followed'})
            else:
                follow.delete()
                return Response({'status': 'user unfollowed'})
            
    @action(detail=True, methods=['delete'], url_path='unfollow')
    def unfollow_user(self, request, pk=None):
        with transaction.atomic():
            user_to_unfollow = self.get_object()
            user = request.user
            follow = Follow.objects.filter(follower=user, following=user_to_unfollow).first()
            if follow:
                follow.delete()
                return Response({'status': 'user unfollowed'})
            else:
                return Response({'status': 'not following this user'}, status=400)

    @action(detail=True, methods=['get'], url_path='posts')
    def posts(self, request, pk=None):
        user = self.get_object()
        posts = Post.objects.filter(author=user).order_by("-like_count","-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='profile')
    def profile(self, request, pk=None):
        user = self.get_object()
        posts = Post.objects.filter(author=user).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='suggestions', permission_classes=[IsAuthenticated])
    def suggestions(self, request, username=None):
        user = User.objects.exclude(id=request.user.id).only('id', 'username', 'display_name').order_by("?")
        four_users = user[:3]
        serializer = self.get_serializer(four_users, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by("-like_count","-created_at").all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        username = self.request.query_params.get('username', None)
        post_id = self.request.query_params.get('postId', None) 
        if user_id:
            return self.queryset.filter(author__id=user_id)
        if username:
            return self.queryset.filter(author__username=username)
        if post_id:
            return self.queryset.filter(id=post_id).select_related('author').prefetch_related('comments')

        return self.queryset


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='like')
    def like_post(self, request, pk=None):
        with transaction.atomic():
            post = self.get_object()
            user = request.user
            like, created = Like.objects.get_or_create(user=user, post=post)
            if created:
                Post.objects.filter(id=post.id).update(like_count=F('like_count') + 1)
                return Response({'status': 'post liked'})
            else:
                like.delete()
                Post.objects.filter(id=post.id).update(like_count=F('like_count') - 1)
                return Response({'status': 'post unliked'})

    @action(detail=False, methods=['get'], url_path='details')
    def details(self, request, pk=None):
        with transaction.atomic():
            res = []
            posts = Post.objects.select_related('author').prefetch_related('comments').all()
            for post in posts:
                pkg = {
                    "id": post.id,
                    "author": post.author.username,
                    "display_name": post.author.display_name,
                    "content": post.content,
                    "created_at": post.created_at,
                    "like_count": post.like_count,
                    "comments": post.comments.all().values("id", "author__username", "author__display_name","content", "created_at")
                }
                res.append(pkg)
            page = self.paginate_queryset(res)
            if page is not None:
                return self.get_paginated_response(page)
            return Response(res)
    

    @action(detail=False, methods=['get'], url_path='feed', permission_classes=[IsAuthenticated])
    def feed(self, request):
        with transaction.atomic():
            user = request.user
            following = Follow.objects.filter(follower=user).values_list('following__id', flat=True)
            posts = Post.objects.filter(author__id__in=following).select_related('author').prefetch_related('comments').order_by("-like_count","-created_at")
            res = []
            for post in posts:
                pkg = {
                    "id": post.id,
                    "author": post.author.username,
                    "display_name": post.author.display_name,
                    "username": post.author.username,
                    "content": post.content,
                    "created_at": post.created_at,
                    "like_count": post.like_count,
                    "comments": post.comments.all().values("id", "author__username", "author__display_name","content", "created_at")
                }
                res.append(pkg)
                
            page = self.paginate_queryset(res)
            if page is not None:
                return self.get_paginated_response(page)
            return Response(res)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        with transaction.atomic():
            user = request.user
            profile = Profile.objects.get(user=user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='(?P<username>\w+)', permission_classes=[IsAuthenticated])
    def page(self, request, username=None):
        with transaction.atomic():
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
