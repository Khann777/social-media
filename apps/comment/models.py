from django.db import models
from apps.post.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
    'self', 
    null=True, 
    blank=True, 
    related_name='answers', 
    on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user}"
        return f"Comment by {self.user}"

