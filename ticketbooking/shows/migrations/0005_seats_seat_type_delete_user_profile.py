# Generated by Django 4.1.5 on 2023-02-03 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0004_bookings_user_profile_shows_seats_bookings_seat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seats',
            name='seat_type',
            field=models.CharField(choices=[('normal', 'normal'), ('executive', 'executive')], default='normal', max_length=20),
        ),
        migrations.DeleteModel(
            name='user_profile',
        ),
    ]
