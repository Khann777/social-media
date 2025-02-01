from django.urls import path
from .views import LikeViewSet

urlpatterns = [
    path('posts/<int:post_id>/like/', LikeViewSet.as_view({'post': 'create'}), name='post-like'),
]
