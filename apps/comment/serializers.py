from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id','post', 'text', 'author', 'parent', 'answers', 'created_at']
        read_only_fields = ['author', 'created_at']

    def get_answers(self, obj):
        answers = obj.answers.all()
        return CommentSerializer(answers, many=True).data
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)