from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('apps.account.urls')),
    path('api/post/', include('apps.post.urls')),
    path('api/comment/', include('apps.comment.urls')),
    path('api/like/', include('apps.like.urls')),
]
