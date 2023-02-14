from rest_framework import serializers
from .models import movies, city, language, Theatre, screen, shows, seats, bookings, booked_seats
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','groups')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        for i in validated_data['groups']: 
            user.groups.add(i)
        user.set_password(validated_data['password'])
        user.save()
        return user



class cityserializer(serializers.ModelSerializer):
    class Meta:
        model = city
        fields = '__all__'


class languageserializer(serializers.ModelSerializer):
    class Meta:
        model = language
        fields = '__all__'


class movieserializer(serializers.ModelSerializer):
    class Meta:
        model = movies
        fields = '__all__'


class theatreserializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = '__all__'


class screenserializer(serializers.ModelSerializer):
    Theatre_id = theatreserializer()
    class Meta:
        model = screen
        fields = '__all__'


class showserializer(serializers.ModelSerializer):
    # movie = movieserializer()
    # screen = screenserializer()
    # language = languageserializer()

    class Meta:
        model = shows
        fields = '__all__'


class seatserializer(serializers.ModelSerializer):
    class Meta:
        model = seats
        fields = '__all__'


class bookingserializer(serializers.ModelSerializer):
    class Meta:
        model = bookings
        fields = '__all__'


class bookedseatserializer(serializers.ModelSerializer):
    class Meta:
        model = booked_seats
        fields = '__all__'

