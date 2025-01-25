from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'post', 'parent', 'created_at') 
    list_filter = ('created_at', 'author') 
    search_fields = ('text', 'author__username', 'post__description')  
    raw_id_fields = ('post', 'parent', 'author')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('post', 'author', 'parent') 

