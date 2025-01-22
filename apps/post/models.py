from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    image = models.ImageField(upload_to='post-images/', blank=True, null=True)
    description = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return f'{self.author}'
    

class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
        )
    
    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f'{self.user} liked post'
    


