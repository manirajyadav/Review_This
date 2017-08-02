from django.shortcuts import render, redirect

from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from imgurpython import ImgurClient
from InstaClone.settings import BASE_DIR
from django.utils import timezone
from paralleldots import set_api_key, sentiment



imgur_CLIENT_ID = "1109a24b0f3855a"
imgur_CLIENT_SECRET = "75c71f0fa4ba69f4f6e6a6a10efa69003d3386a1"


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
    response_data['message']= ' Fill in your details.'
    if request.method == "POST":
        form = LoginForm( request.POST )
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user= UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie( key='session_token', value=token.session_token )
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'
            else:
                response_data['message']= 'Sorry! The User You Entered Does Not Exist.'


    else:
        form = LoginForm()

    response_data['form']= form

    return render(request, 'login.html', response_data)


def post_view(request):
  user = check_validation(request)

  if user:
    if request.method == 'GET':
      form = PostForm()


    elif request.method == 'POST':
        form = PostForm( request.POST, request.FILES )
        if form.is_valid():
            image = form.cleaned_data.get( 'image' )
            caption = form.cleaned_data.get( 'caption' )

            post = PostModel( user=user, image=image, caption=caption )
            post.save()
            path = str( BASE_DIR +"/"+ post.image.url )
            client = ImgurClient( imgur_CLIENT_ID, imgur_CLIENT_SECRET)
            post.image_url = client.upload_from_path( path, anon=True )['link']
            post.save()
            return redirect( '/feed/' )


    return render( request, 'post.html', {'form': form} )

  else:
    return redirect('/login/')


def feed_view(request):

    user = check_validation( request )
    if user:
        posts = PostModel.objects.all().order_by( '-created_on' )
        for post in posts:
            set_api_key( 'C2TJEgxONUsOJgbfTRzJZk896mQDzl5aADdNQrYzJrQ' )

            text = post.caption
            response = sentiment(text)
            if response['sentiment'] > 0.5:
                message = 'Positive'
            else:
                message = 'Negative'



            existing_like = LikeModel.objects.filter( post_id=post.id, user=user ).exists()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html',{'posts': posts, 'message': message})
    else:
        return redirect( '/login/' )

def logout_view(request):
    x= SessionToken.objects.filter( session_token=request.COOKIES.get( 'session_token' ) ).first()
    x.is_valid= False
    x.save()
    return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()

            return redirect('/feed/')

    else:
        return redirect('/login/')

def comment_view(request):
    user = check_validation( request )
    if user and request.method == 'POST':
        form = CommentForm( request.POST )
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create( user=user, post_id=post_id, comment_text=comment_text )
            comment.save()
            return redirect( '/feed/' )
        else:
            return redirect( '/feed/' )
    else:
        return redirect( '/login' )

# For validating the session
def check_validation(request):
    if request.COOKIES.get( 'session_token' ):
        session = SessionToken.objects.filter( session_token=request.COOKIES.get( 'session_token' ) ).first()
        if session:
            if session.is_valid == True:
                time_to_live = session.created_on + timedelta( days=1 )
                if time_to_live > timezone.now():
                    return session.user

    else:
        return None




