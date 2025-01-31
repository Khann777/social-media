from django.urls import path
from .views import LikeViewSet

urlpatterns = [
    path('like/<int:post_id>/', LikeViewSet.as_view({'post': 'create'}), name='post-like'),
]
