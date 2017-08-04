
from __future__ import unicode_literals

from django.db import models
import uuid, datetime

# creating model to make a new signup and save details
class UserModel(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    email = models.EmailField(null=True)
    username = models.CharField( max_length=120,unique=True, null=False, blank=False)
    password = models.CharField( max_length=120)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField( auto_now=True, null=True)

# creating model to save session tokens for logged in users
class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    # creating alphanumeric token
    def create_token(self):
        self.session_token = uuid.uuid4()

# model for making new posts with image and captions and saving user's like
class PostModel(models.Model):
  user = models.ForeignKey(UserModel)
  image = models.FileField(upload_to='user_images')
  image_url = models.CharField(max_length=255)
  caption = models.CharField(max_length=240)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  has_liked = False
  # couting likes
  @property
  def like_count(self):
      return len( LikeModel.objects.filter( post=self ) )
  # saving comments for particular post
  @property
  def comments(self):
      return CommentModel.objects.filter( post=self ).order_by('created_on')

# making like on posts and storing
class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

# making comments on the posts and storing
class CommentModel(models.Model):
  user = models.ForeignKey(UserModel)
  post = models.ForeignKey(PostModel)
  comment_text = models.CharField(max_length=555)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)