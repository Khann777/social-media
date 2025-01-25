from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField()
    answers = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'parent', 'answers', 'created_at']

    def get_answers(self, obj):
        answers = obj.answers.all()
        return CommentSerializer(answers, many=True).data
