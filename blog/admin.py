from django.contrib import admin
from .models import Post

# CUSTOMIZING THE DJANGO-ADMIN
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Customizin the django-admin for Post Model"""
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = [
        'status', 'created', 'publish', 'author'
    ]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']