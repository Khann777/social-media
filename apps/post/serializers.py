from rest_framework import serializers
from .models import Post, Like
from comment.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField()
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'image', 'author', 'created_at', 'view_count', 'comments', 'likes_count']

    def get_comments(self, instance):
        comments = instance.comments.all()
        if comments:
            return CommentSerializer(comments, many=True).data
        return None

    def get_likes_count(self, obj):
        return obj.likes.count()
