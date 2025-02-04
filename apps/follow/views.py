from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()

class FollowView(generics.CreateAPIView):
    """Позволяет пользователю подписаться на другого пользователя"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        following = get_object_or_404(User, username=self.kwargs.get("username"))
        if Follow.objects.filter(follower=request.user, following=following).exists():
            return Response({"detail": "Вы уже подписаны на этого пользователя."}, status=status.HTTP_400_BAD_REQUEST)

        subscription = Follow.objects.create(follower=request.user, following=following)
        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnFollowView(generics.DestroyAPIView):
    """Позволяет пользователю отписаться от другого пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        following = get_object_or_404(User, username=self.kwargs.get("username"))
        subscription = Follow.objects.filter(follower=request.user, following=following)
        if subscription.exists():
            subscription.delete()
            return Response({"detail": "Вы успешно отписались."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Вы не подписаны на этого пользователя."}, status=status.HTTP_400_BAD_REQUEST)


class ListFollowersView(generics.ListAPIView):
    """Список подписчиков пользователя"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Follow.objects.filter(following=user)


class ListFollowingView(generics.ListAPIView):
    """Список пользователей, на которых подписан пользователь"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Follow.objects.filter(follower=user)
