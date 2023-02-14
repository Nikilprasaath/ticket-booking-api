"""ticketbooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shows.views import signupview, listcities, listmovies, editmovies, editcities, listlanguage, editlanguage, show, listshows, booking, adminlogin, userbookings, listtheatre, listscreen, listseats, bookedseats, login, adminsignupview, edittheatre, editscreen
from shows import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login',login.as_view()),
    path('signup',signupview.as_view()),

    path('adminlogin',adminlogin.as_view()),
    path('adminsignup',adminsignupview.as_view()),

    path('',listcities.as_view()),
    path('listlanguage',listlanguage.as_view()),
    path('movielist',listmovies.as_view()),
    path('listtheatres',listtheatre.as_view()),
    path('listscreen',listscreen.as_view()),
    path('shows',listshows.as_view()),
    path('listseats',listseats.as_view()),
    path('bookedseatslist',bookedseats.as_view()),
    path('userbookings',userbookings.as_view()),

    path('editcities',editcities.as_view()),
    path('editcities/<int:city_id>',editcities.as_view()),
    path('editmovie',editmovies.as_view()),
    path('editmovie/<int:movie_id>',editmovies.as_view()),
    path('editlanguage',editlanguage.as_view()),
    path('editlanguage/<int:lang_id>',editlanguage.as_view()),
    path('edittheatre',edittheatre.as_view()),
    path('edittheatre/<int:theatre_id>',edittheatre.as_view()),
    path('editscreen',editscreen.as_view()),
    path('editscreen/<int:screen_id>',editscreen.as_view()),
    path('editshows',show.as_view()),
    path('editshows/<int:id>',show.as_view()),
    path('booking',booking.as_view()),
    
]