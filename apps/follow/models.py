from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count

User = get_user_model()

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        help_text="Пользователь, который подписывается"
    )
    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE,
        help_text="Пользователь, на которого подписываются"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower} → {self.following}"
