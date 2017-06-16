from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'photo']

admin.site.register(Post, PostAdmin)
