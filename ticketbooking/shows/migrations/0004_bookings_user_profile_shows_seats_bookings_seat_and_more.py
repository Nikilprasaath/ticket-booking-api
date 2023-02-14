# Generated by Django 4.1.5 on 2023-02-03 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shows', '0003_alter_movies_city_alter_movies_language_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'active'), ('not active', 'not active')], default='active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='user_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookings', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shows.bookings')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='shows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_time', models.DateTimeField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.language')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.movies')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.screen')),
            ],
        ),
        migrations.CreateModel(
            name='seats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_no', models.IntegerField()),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.shows')),
            ],
        ),
        migrations.AddField(
            model_name='bookings',
            name='seat',
            field=models.ManyToManyField(to='shows.seats'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shows.shows'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='booked_seats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shows.bookings')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shows.screen')),
                ('seat_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='shows.seats')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shows.shows')),
            ],
        ),
    ]
