from django.shortcuts import render, redirect

from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from imgurpython import ImgurClient
from InstaClone.settings import BASE_DIR
from django.utils import timezone
from paralleldots import set_api_key, sentiment


# saving imgur client id and secret in variables
imgur_CLIENT_ID = "1109a24b0f3855a"
imgur_CLIENT_SECRET = "75c71f0fa4ba69f4f6e6a6a10efa69003d3386a1"

# creating controller for signing in
def signup_view(request):
    today = datetime.now()
    if request.method == "POST":
        form = SignUpForm( request.POST )
        # checking for valid form
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            # making password hashed in database
            user = UserModel( name=name, password=make_password(password), email=email, username=username )
            user.save()
            return render(request, 'success.html')
            # return redirect('login/')
    # else if request is get
    else:
        form = SignUpForm()
    # redirecting to index.html
    return render(request, 'index.html', {'form': form,'today': today})

# creating controller for login
def login_view(request):
    response_data = {}
    response_data['message']= ' Fill in your details.'
    if request.method == "POST":
        form = LoginForm( request.POST )
        # if form is valid
        if form.is_valid():
            # accessing the entered username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user= UserModel.objects.filter(username=username).first()
            # searching the user and matching the password with hashed password
            if user:
                if check_password(password, user.password):
                    # saving the session token if password matched
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    # redirecting to show post of others
                    response = redirect('/feed/')
                    # setting session token in cookie
                    response.set_cookie( key='session_token', value=token.session_token )
                    return response
                # if password does not match
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'
            # user not found
            else:
                response_data['message']= 'Sorry! The User You Entered Does Not Exist.'

    # if getting get request
    else:
        form = LoginForm()

    response_data['form']= form
    # sending to login page
    return render(request, 'login.html', response_data)

# creating controller for making a new post
def post_view(request):
  # checking whether user is logged in
  user = check_validation(request)
  # if user is logged in
  if user:
    if request.method == 'GET':
      form = PostForm()


    elif request.method == 'POST':
        form = PostForm( request.POST, request.FILES )
        # if form is valid
        if form.is_valid():
            # getting the form filled by user
            image = form.cleaned_data.get( 'image' )
            caption = form.cleaned_data.get( 'caption' )
            # saving post in DB
            post = PostModel( user=user, image=image, caption=caption )
            post.save()
            # uploading to imagur for further use
            path = str( BASE_DIR +"/"+ post.image.url )
            client = ImgurClient( imgur_CLIENT_ID, imgur_CLIENT_SECRET)
            post.image_url = client.upload_from_path( path, anon=True )['link']
            post.save()
            # redirecting to feeds
            return redirect( '/feed/' )


    return render( request, 'post.html', {'form': form} )
  # if not logged in then send to login page
  else:
    return redirect('/login/')

# creating controller to view posts
def feed_view(request):
    set_api_key( 'C2TJEgxONUsOJgbfTRzJZk896mQDzl5aADdNQrYzJrQ' )
    # check whether used is logged in
    user = check_validation( request )
    if user:
        # sort posts in ascending order of time
        posts = PostModel.objects.all().order_by( '-created_on' )
        # iterating through all posts
        for post in posts:
            # setting api for parallel dots to analyse sentiments
            message = []
            # checking whether comment is positive or negative

            if post.caption!= None:

                response = sentiment(str(post.caption))

                if response['sentiment'] >= 0.5:
                    post.review = 'Positive'
                elif response['sentiment']< 0.5:
                    post.review = 'Negative'
            # checking for existing like
            existing_like = LikeModel.objects.filter( post_id=post.id, user=user ).exists()
            if existing_like:
                post.has_liked = True
        # redirecting to feeds
        return render(request, 'feed.html',{'posts': posts})
    # if user not logged in
    else:
        return redirect( '/login/' )
# logging out controller
def logout_view(request):
    x= SessionToken.objects.filter( session_token=request.COOKIES.get( 'session_token' ) ).first()
    x.is_valid= False
    x.save()
    # redirecting to login page
    return redirect('/login/')
# controller for liking a post
def like_view(request):
    # checking whether user is logged in
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        # if form is valid
        if form.is_valid():
            # getting post id
            post_id = form.cleaned_data.get('post').id
            # checking for existing like
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            # if hasent liked before then make a like
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            # liked before then delete the like
            else:
                existing_like.delete()

            # redirecting to feed
            return redirect('/feed/')
    # not logged in so redirecting to login page
    else:
        return redirect('/login/')

# creating controller for commenting
def comment_view(request):
    # checking whether user is logged in
    user = check_validation( request )
    if user and request.method == 'POST':
        form = CommentForm( request.POST )
        # if form is valid
        if form.is_valid():
            # accessing the form filled by user
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            # saving in database
            comment = CommentModel.objects.create( user=user, post_id=post_id, comment_text=comment_text )
            comment.save()
            # redirecting to feeds
            return redirect( '/feed/' )
        else:
            return redirect( '/feed/' )
    # if user isnt logged in
    else:
        return redirect( '/login' )

# For validating the session
def check_validation(request):

    if request.COOKIES.get( 'session_token' ):
        session = SessionToken.objects.filter( session_token=request.COOKIES.get( 'session_token' ) ).first()
        # if there exist the session token
        if session:
            # checking whether the session of user still exist
            if session.is_valid == True:
                time_to_live = session.created_on + timedelta( days=1 )
                if time_to_live > timezone.now():
                    return session.user

    else:
        return None




