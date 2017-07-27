
from __future__ import unicode_literals

from django.db import models
import uuid, datetime


class UserModel(models.Model):
    name = models.CharField(max_length=120,unique=True, null=False, blank=False)
    email = models.EmailField(null=True)
    username = models.CharField( max_length=120,unique=True, null=False, blank=False)
    password = models.CharField( max_length=120)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField( auto_now=True, null=True)


class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()


class PostModel(models.Model):
  user = models.ForeignKey(UserModel)
  image = models.FileField(upload_to='user_images')
  image_url = models.CharField(max_length=255)
  caption = models.CharField(max_length=240)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
