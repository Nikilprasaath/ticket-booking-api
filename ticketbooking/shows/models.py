from django.db import models
from django.contrib.auth.models import User


class city(models.Model):
    city = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.city


class language(models.Model):
    language = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.language


class movies(models.Model):
    rating_choice = (
        ('U', 'U'),
        ('UA', 'U/A'),
        ('A', 'A'),
        ('R', 'R'),
    )
    movie_name = models.CharField(max_length=30)
    director = models.CharField(max_length=20)
    cast = models.CharField(max_length=100)
    certification = models.CharField(max_length=3, choices=rating_choice)
    city = models.ManyToManyField(city, related_name='mov_city')
    language = models.ManyToManyField(language, related_name='mov_lang')

    def __str__(self):
        return self.movie_name


class Theatre(models.Model):
    name = models.CharField(max_length=20)
    city = models.ManyToManyField(city, related_name= 'theatre_city')
    screens = models.IntegerField()

    def __str__(self):
        return self.name


class screen(models.Model):
    Theatre_id = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name= 'theatre_screen')
    screen_no = models.IntegerField()
    normal_seat_count = models.IntegerField()
    normal_seat_price = models.IntegerField()
    executive_seat_count = models.IntegerField(default=120)
    executive_seat_price = models.IntegerField(default=190)

    def __str__(self):
        return "%s | %s" % (self.Theatre_id, self.screen_no)


class shows(models.Model):
    movie = models.ForeignKey(movies,on_delete=models.CASCADE)
    screen = models.ForeignKey(screen,on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    language = models.ForeignKey(language, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.id)


class seats(models.Model):
    choices = (
        ('normal','normal'),
        ('executive','executive')
    )
    show = models.ForeignKey(shows, on_delete= models.CASCADE)
    seat_no = models.IntegerField()
    seat_type = models.CharField(max_length=20, choices= choices,default='normal')
    price = models.IntegerField(default= 0)

    def __str__(self):
        return (str(self.show.movie.movie_name) + str(self.seat_no))


class bookings(models.Model):
    status_choice=(
        ('active','active'),
        ('not active', 'not active')
    )
    payment_choice=(
        ('failed','failed'),
        ('pending','pending'),
        ('confirmed','confirmed')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    show = models.ForeignKey(shows, on_delete=models.DO_NOTHING)
    seat = models.ManyToManyField(seats)
    status = models.CharField(max_length=10, choices= status_choice, default='active')
    payment_confirmation = models.CharField(max_length=20,choices= payment_choice, default='pending')
    total_price = models.IntegerField(default= 0)

    def __str__(self):
        return self.user.first_name


class booked_seats(models.Model):
    booking = models.ForeignKey(bookings, on_delete=models.DO_NOTHING)
    show = models.ForeignKey(shows, on_delete=models.DO_NOTHING)
    seat_id = models.OneToOneField(seats, on_delete=models.DO_NOTHING)
    screen = models.ForeignKey(screen, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id)


