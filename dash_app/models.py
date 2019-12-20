from django.db import models
import re
from django.contrib import messages
from django.contrib.messages import get_messages

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, request):
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, 'Invalid email')

        if len(request.POST['first_name']) < 1:
            messages.error(request, 'Name should be more than 1 character')

        if len(request.POST['last_name']) < 1:
            messages.error(request, 'Last name should be more than 1 character')
        
        if len(request.POST['password']) <= 5:
            messages.error(request, 'Password should be more than 5 characters')

        if request.POST['password'] != request.POST['password_confirm']:
            messages.error(request, 'Passwords should match')

        error_messages = messages.get_messages(request)
        error_messages.used = False
        return len(error_messages) == 0

class User(models.Model):
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=25)
    desc = models.TextField()
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class PostManager(models.Manager):
    def post_validator(self, request):
        if len(request.POST['post']) <= 1:
            messages.error(request, 'Please write more than 1 character')

        error_messages = messages.get_messages(request)
        error_messages.used = False
        return len(error_messages) == 0

class Post(models.Model):
    post = models.TextField()
    created_by = models.ForeignKey('User', related_name='users_post', on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class CommentManager(models.Manager):
    def comment_validator(self, request):
        if len(request.POST['comment']) <= 1:
            messages.error(request, 'Please write more than 1 character')

        error_messages = messages.get_messages(request)
        error_messages.used = False
        return len(error_messages) == 0

class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete='CASCADE')
    created_by = models.ForeignKey('User', related_name='users_comment', on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()




