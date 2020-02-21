from django.contrib import admin

from .models import Post, Comment, Like, ContactMessage

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(ContactMessage)
# Register your models here.
