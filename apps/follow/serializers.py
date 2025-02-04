from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_following(self, value):
        """Проверяем, чтобы пользователь не подписался на самого себя"""
        if self.context["request"].user == value:
            raise serializers.ValidationError("Нельзя подписаться на самого себя.")
        return value
