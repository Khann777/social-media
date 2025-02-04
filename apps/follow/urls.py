from django.urls import path
from .views import FollowView, UnFollowView, ListFollowersView, ListFollowingView

urlpatterns = [
    path('follow/<str:username>/', FollowView.as_view(), name='follow'),
    path('unfollow/<str:username>/', UnFollowView.as_view(), name='unfollow'),
    path('followers/<str:username>/', ListFollowersView.as_view(), name='list_followers'),
    path('following/<str:username>/', ListFollowingView.as_view(), name='list_following'),
]
