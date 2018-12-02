from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from mysite.views import login_procedure, edit_profile, change_password, change_password2

urlpatterns = [
    url(r'^login/$', login_procedure, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'), #This is an inbuilt function for logging out
    url(r'^admin/', admin.site.urls),
    url(r'^', include('mysite.urls')),
    url(r'^profile/edit/$', edit_profile, name='edit-profile'),

    url(r'^change-password/$', change_password, name='change-password'),
    url(r'^/profile/edit/password/$', change_password2, name='change-password2'),
]
