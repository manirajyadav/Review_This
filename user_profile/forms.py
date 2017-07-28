from django import forms
from models import UserModel,PostModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email','username','name','password']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=40)


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image','caption']