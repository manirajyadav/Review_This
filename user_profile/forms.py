from django import forms
from models import UserModel,PostModel, LikeModel, CommentModel

# form for signup
class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email','username','name','password']


# form for login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=40)

# form for making a new post
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image','caption']


class LikeForm( forms.ModelForm ):
    class Meta:
        model = LikeModel
        fields = ['post']


class CommentForm(forms.ModelForm):
  class Meta:
    model = CommentModel
    fields = ['comment_text', 'post']

class SearchForm(forms.Form):
    username = forms.CharField( max_length=120 )