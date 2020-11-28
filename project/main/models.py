from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 50)
    pub_date = models.DateField('date published')
    body = models.TextField()
    board = models.IntegerField(default=0)
    def __str__(self):
        return self.title #관리 시 확인하기 편리
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # db_column = post_id
    content = models.TextField()
    def __str__(self):
        return self.content

class Blog(models.Model):
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 25)
    title = models.CharField(max_length = 50)
    pub_date = models.DateField('date published')
    body = models.TextField()
    def __str__(self):
        return self.title

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 25)