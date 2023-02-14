from django.contrib import admin
from .models import movies, city, language, Theatre, screen, shows, seats, bookings, booked_seats
from django.contrib.admin.options import ModelAdmin

class movieadmin(ModelAdmin):
    model=movies
    list_display = ['movie_name', 'id']

class cityadmin(ModelAdmin):
    model = city
    list_display = ['city','id']

class languageadmin(ModelAdmin):
    model = language
    list_display = ['id','language']

class theatreadmin(ModelAdmin):
    model = Theatre
    list_display = ['id','name']

class screenadmin(ModelAdmin):
    model = screen
    list_display = ['id','Theatre_id','screen_no']

class showadmin(ModelAdmin):
    model= shows
    list_display = ['id','movie','screen','show_time']

class seatadmin(ModelAdmin):
    model = seats
    list_display = ['id','show','seat_no','seat_type']

class booked_seat_admin(ModelAdmin):
    model = booked_seats
    list_display = ['id','booking','show','seat_id']

class bookingsadmin(ModelAdmin):
    model = bookings
    list_display = ['id','user','show','status']

    
admin.site.register(movies, movieadmin)
admin.site.register(city, cityadmin)
admin.site.register(language, languageadmin)
admin.site.register(Theatre, theatreadmin)
admin.site.register(screen, screenadmin)
admin.site.register(shows, showadmin)
admin.site.register(seats, seatadmin)
admin.site.register(bookings, bookingsadmin)
admin.site.register(booked_seats, booked_seat_admin)
