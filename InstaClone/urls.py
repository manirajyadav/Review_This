# importing libraries
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from user_profile.views import signup_view, login_view, feed_view,post_view,logout_view,like_view,comment_view,search_view

# adding all the urls
urlpatterns = [
    url('admin/', admin.site.urls),
    url('search/', search_view),
    url('logout/', logout_view),
    url('like/', like_view),
    url('post/', post_view),
    url('comment/', comment_view),
    url('feed/', feed_view),
    url('login/', login_view),
    url('', signup_view)
]
