from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.post.models import Post
from .models import Like
from .serializers import LikeSerializer

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, post_id=None):
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Пост не найден"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()
            return Response({"message": "Лайк удалён"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "Пост лайкнут"}, status=status.HTTP_201_CREATED)
