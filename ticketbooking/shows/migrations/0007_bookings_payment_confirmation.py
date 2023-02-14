# Generated by Django 4.1.5 on 2023-02-06 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0006_screen_executive_seat_price_screen_normal_seat_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='payment_confirmation',
            field=models.CharField(choices=[('failed', 'failed'), ('pending', 'pending'), ('confirmed', 'confirmed')], default='pending', max_length=20),
        ),
    ]
