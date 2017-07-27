from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm
from models import UserModel, SessionToken, PostModel
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.utils import timezone


def signup_view(request):
    today = datetime.now()
    if request.method == "POST":
        form = SignUpForm( request.POST )
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = UserModel( name=name, password=make_password(password), email=email, username=username )
            user.save()
            return render(request, 'success.html')
            # return redirect('login/')
    else:


        form = SignUpForm()

    return render(request, 'index.html', {'form': form,'today': today})


def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm( request.POST )
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user= UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken( user=user )
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie( key='session_token', value=token.session_token )
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'
            else:
                response_data['message']= 'User Does Not Exist'


    else:
        form = LoginForm()

    response_data['form']= form

    return render(request, 'login.html', response_data)


def post_view(request):
  user = check_validation(request)

  if user:
    if request.METHOD == 'GET':
      form = PostForm()


    elif request.METHOD == 'POST':
        form = PostForm( request.POST, request.FILES )
        if form.is_valid():
            image = form.cleaned_data.get( 'image' )
            caption = form.cleaned_data.get( 'caption' )

            post = PostModel( user=user, image=image, caption=caption )
            post.save()

    return render( request, 'post.html', {'form': form} )

  else:
    return redirect('/login/')


def feed_view(request):
    return render( request, 'feed.html' )


# For validating the session
def check_validation(request):
    if request.COOKIES.get( 'session_token' ):
        session = SessionToken.objects.filter( session_token=request.COOKIES.get( 'session_token' ) ).first()
        if session:
            return session.user
    else:
        return None




