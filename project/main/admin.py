from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Post, Comment, Subject, Blog

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 3

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]

admin.site.register(Post, PostAdmin)


admin.site.register(Subject)
admin.site.register(Blog)
#admin.site.register(Comment)