from rest_framework import serializers
from .models import Post, Like
from apps.comment.serializers import CommentSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'description', 'image', 'author', 'created_at', 'view_count', 'comments', 'likes_count']

    def get_comments(self, instance):
        comments = instance.comments.all()
        if comments:
            return CommentSerializer(comments, many=True).data
        return None

    def get_likes_count(self, obj):
        return obj.likes.count()
