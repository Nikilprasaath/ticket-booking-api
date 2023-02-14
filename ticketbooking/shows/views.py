from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from knox.views import LoginView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import generics, mixins
from .models import movies, city, language, Theatre, screen, shows, seats, bookings, booked_seats
from .serializer import movieserializer, cityserializer, languageserializer, theatreserializer, screenserializer, RegisterSerializer, showserializer, seatserializer, bookingserializer, bookedseatserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, DjangoModelPermissions
from knox.views import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime
from .scheduler import *
  



class adminpermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(id=2):
            return True

        return False
        

class userpermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(id=1):
            return True

        return False


class signupview(APIView):
    def post(self, request):
        request.data['groups']=[1]
        serial = RegisterSerializer(data= request.data)
        if serial.is_valid():
            serial.save()
            return Response("User created", status= status.HTTP_201_CREATED)
        return Response(serial.errors, status= status.HTTP_400_BAD_REQUEST)
    

class adminsignupview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, adminpermission]

    def post(self,request):
        request.data['groups']=[2]
        serial  =RegisterSerializer(data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response("admin user created", status=status.HTTP_201_CREATED)
        

class login(LoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, userpermission]


class adminlogin(LoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, adminpermission]


class listcities(generics.ListAPIView):
    queryset = city.objects.all()
    serializer_class = cityserializer
    # permission_classes = [DjangoModelPermissions]


class listlanguage(generics.ListAPIView):
    serializer_class = languageserializer
    queryset = language.objects.all()


class listmovies(generics.ListAPIView):
    queryset = movies.objects.all()
    serializer_class = movieserializer

    def get(self, request):
        language = request.query_params.get('language')
        city = request.query_params.get('city')
        # theatre = request.query_params.get('theatre')



        if language and city:
            set = movies.objects.filter(city = city, language = language)

        # if city and theatre:
            # set = movies.objects.filter(city = city )

        elif city:
            set = movies.objects.filter(city = city)

        elif language:
            set = movies.objects.filter(language = language)

        else:
            set = movies.objects.all()
        
        serial = movieserializer(set, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)



class listtheatre(generics.ListAPIView):
    queryset= Theatre.objects.all()
    serializer_class = theatreserializer

    def get(self, request):
        city = request.query_params.get('city')

        if city:
            set = Theatre.objects.filter(city = city)

        else:
            set = Theatre.objects.all()

        serial = theatreserializer(set, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)



class listscreen(generics.ListAPIView):
    queryset = screen.objects.all()
    serializer_class = screenserializer

    def get(self, request):
        theatre = request.query_params.get('theatre')

        if theatre:
            set = screen.objects.filter(Theatre_id = theatre)

        else:
            set = screen.objects.all()

        serial = screenserializer(set, many = True)
        return Response(serial.data, status= status.HTTP_200_OK)



class listshows(generics.ListAPIView):
    queryset = shows.objects.all()
    serializer_class = showserializer

    def get(self, request):
        theatre = request.query_params.get('theatre')
        language = request.query_params.get('language')
        movie = request.query_params.get('movie')

        now = datetime.datetime.now()
        now1 = timezone.now()

        screen_id = screen.objects.filter(Theatre_id = theatre)
        list1 = list(screen_id)
        screen_ids = [x.id for x in list1]

        if theatre and language and movie:
            set = shows.objects.filter(screen__in = screen_ids, movie = movie, language = language, show_time__gte = now)

        elif theatre and movie:
            set = shows.objects.filter(screen__in = screen_ids, movie = movie, show_time__gte = now)

        elif theatre:
            set = shows.objects.filter(screen__in = screen_ids, show_time__gte = now)

        elif movie:
            set = shows.objects.filter(movie = movie, show_time__gte = now)

        else:
            return Response("params not given",status= status.HTTP_400_BAD_REQUEST)

        serial = showserializer(set, many=True)

        # print(list1)
        # print(list1[1].id)
        # print(screen_ids)

        return Response(serial.data, status= status.HTTP_200_OK)



class listseats(generics.ListAPIView):
    queryset = seats.objects.all()
    serializer_class = seatserializer

    def get(self, request):
        show = request.query_params.get('show')

        if show:
            set = seats.objects.filter(show= show)

        else:
            return Response("show id not mentioned", status= status.HTTP_400_BAD_REQUEST)

        serial = seatserializer(set, many=True)
        return Response(serial.data, status= status.HTTP_200_OK)
    


class bookedseats(generics.ListAPIView):
    queryset = booked_seats.objects.all()
    serializer_class = bookedseatserializer

    def get(self, request):
        show = request.query_params.get('show')

        if show:
            set = booked_seats.objects.filter(show = show)

        else:
            return Response("show id not mentioned", status= status.HTTP_400_BAD_REQUEST)
        
        serial = bookedseatserializer(set, many= True)
        return Response(serial.data, status= status.HTTP_200_OK)
    


class userbookings(generics.GenericAPIView):
    queryset = bookings.objects.all()
    serializer_class = bookingserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, userpermission]

    def get(self, request):
        id = request.user.id

        set = bookings.objects.filter(user = id)
        serial = bookingserializer(set, many= True)

        return Response(serial.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        request.data['user'] = request.user.id

        seats_in_req = request.data['seat']

        for i in seats_in_req:
            if seats.objects.get(id = i).show.id != request.data['show']:
                return Response("show "+str(request.data['show'])+" does not have the seat id", status= status.HTTP_400_BAD_REQUEST)
            
            
            if booked_seats.objects.filter(seat_id = i):
                return Response(str(i)+' is already booked', status= status.HTTP_400_BAD_REQUEST) 
                

        serial = bookingserializer(data= request.data)
        serial.is_valid(raise_exception=True)
        serial.save()

        # It is determined by the confirmation of the payment
        payment_status = 'success'

        id = serial.data['id']
        booking_obj = bookings.objects.get(id = id)
         
        if payment_status == 'success':
            booking_obj.payment_confirmation = 'confirmed'
            
            show_id = request.data['show']
            show = shows.objects.get(id= show_id)
            screen_obj = show.screen
    

            seat_id_set = booking_obj.seat.all().values()

            for seat in seat_id_set:
                seat_id = seat['id']
                seat_obj = seats.objects.get(id=seat_id)

                seat = booked_seats.objects.create(booking = booking_obj, 
                                                   show = show, 
                                                   seat_id = seat_obj, 
                                                   screen = screen_obj)
                
                seat.save()
  
        else:
            booking_obj.payment_confirmation = 'failed'

        booking_obj.save()

        return Response(serial.data, status= status.HTTP_200_OK)
    

    def delete(self, request):
        if request.data:
            id = request.data['id']
            obj = bookings.objects.get(id = id)
            obj.delete()
            return Response('Deleted Successfully', status= status.HTTP_200_OK)





# employee user views

class editcities(generics.GenericAPIView):
    queryset = city.objects.all()
    serializer_class = cityserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]

    def get_object(self,city_id):
        try:
            return city.objects.get(id=city_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,city_id=None):
        print(city_id)
        if not city_id:
            city_obj = city.objects.all()
            serial= cityserializer(city_obj, many= True)
            return Response(serial.data)

        city_obj = self.get_object(city_id=city_id)
        serial=cityserializer(city_obj)
        return Response(serial.data)

    def post(self,request):
        serial=cityserializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data,status= status.HTTP_201_CREATED)

        return Response(serial.errors, status= status.HTTP_400_BAD_REQUEST)

    def put(self,request,city_id):
        if city_id:
            city_obj = self.get_object(city_id=city_id)
            serial = cityserializer(city_obj, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(status= status.HTTP_400_BAD_REQUEST)

    def delete(self,request,city_id):
        if city_id:
            city_obj = self.get_object(city_id=city_id)
            city_obj.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)



class editmovies(generics.GenericAPIView):
    queryset = movies.objects.all()
    serializer_class = movieserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]


    def get_object(self,movie_id):
        try:
            return movies.objects.get(id = movie_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    
    def get(self,request,movie_id=None):
        print(movie_id)
        if not movie_id:
            movie_obj = movies.objects.all()
            serial= movieserializer(movie_obj, many= True)
            return Response(serial.data)

        movie_obj = self.get_object(movie_id=movie_id)
        
        serial=movieserializer(movie_obj)
        
        return Response(serial.data)


    def post(self,request):
        serial=movieserializer(data=request.data)
        # print(request.data)
        
        if serial.is_valid():
            serial.save()
            return Response(serial.data,status= status.HTTP_201_CREATED)
        
        return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,movie_id):
        if movie_id:
            movie_obj = self.get_object(movie_id=movie_id)
            serial = movieserializer(movie_obj, data=request.data)
            serial.is_valid(raise_exception= True)
            serial.save()
            return Response(serial.data)
        return Response("id not mentioned",status= status.HTTP_400_BAD_REQUEST)


    def delete(self,request,movie_id):
        if movie_id:
            movie_obj = self.get_object(movie_id)
            movie_obj.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)



class editlanguage(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = language.objects.all()
    serializer_class = languageserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]
    lookup_field = None or 'lang_id'

    def get_object(self):
        filterk = {'id':self.lang_id}
        obj = language.objects.all()
        obj1 = get_object_or_404(obj,**filterk)
        return obj1

    def get(self, request, lang_id = None):
        self.lang_id = lang_id
        if lang_id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, lang_id):
        self.lang_id = lang_id
        return self.update(request)

    def delete(self, request, lang_id):
        self.lang_id = lang_id
        return self.destroy(request)




class edittheatre(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Theatre.objects.all()
    serializer_class = theatreserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]
    lookup_field = None or 'theatre_id'


    def get_object(self):
        filterk = {'id':self.theatre_id}
        obj = Theatre.objects.all()
        obj1 = get_object_or_404(obj,**filterk)
        return obj1

    def get(self, request, theatre_id = None):
        self.theatre_id = theatre_id
        if theatre_id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, theatre_id):
        self.theatre_id = theatre_id
        return self.update(request,id=id)

    def delete(self, request, theatre_id):
        self.theatre_id = theatre_id
        return self.destroy(request, id=id)



class editscreen(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = screen.objects.all()
    serializer_class = screenserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]
    lookup_field = None or 'screen_id'


    def get_object(self):
        kfilter = {'id':self.screen_id}
        obj = screen.objects.all()
        obj1 = get_object_or_404(obj,**kfilter)
        return obj1

    def get(self, request, screen_id = None):
        self.screen_id = screen_id
        if screen_id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, screen_id):
        self.screen_id = screen_id
        return self.update(request)

    def delete(self, request, screen_id):
        self.screen_id = screen_id
        return self.destroy(request)



class show(generics.GenericAPIView):
    serializer_class = showserializer
    queryset = shows.objects.all()
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]


    def get_object(self,id):
        try:
            obj = shows.objects.get(id=id)
            return obj
        except:
            return Response(" object not found",status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        if request.data:
            
            id= request.data['id']
            print(id)
            obj = self.get_object(id)
            
            serial = showserializer(obj)
            return Response(serial.data, status= status.HTTP_200_OK)

        set = shows.objects.all()
        serial = showserializer(set, many=True)
        return Response(serial.data,status=status.HTTP_200_OK) 
        

    def post(self, request):
        
        serial = showserializer(data = request.data)
        serial.is_valid(raise_exception=True)
        serial.save()

        id = serial.data['id']
        show_obj= shows.objects.get(id=id)
        screen_id=serial.data['screen']

        screen_obj = screen.objects.get(id=screen_id)

        exec_seats = screen_obj.executive_seat_count
        normal_seats = screen_obj.normal_seat_count

        exec_seat_price = screen_obj.executive_seat_price
        normal_seat_price = screen_obj.normal_seat_price

        for i in range(1,exec_seats+1):
            seats.objects.create(seat_no = i, show = show_obj, seat_type = "executive", price = exec_seat_price)

        for i in range(1,normal_seats+1):
            seats.objects.create(seat_no = i, show = show_obj, seat_type = "normal", price = normal_seat_price)

        return Response(serial.data, status= status.HTTP_200_OK)
        

    def put(self, request):
        if request.data:
            id = request.data['id']
            obj = shows.objects.get(id = id)
            serial = showserializer(obj, data=request.data)
            serial.is_valid(raise_exception=True)
            serial.save()
            return Response(serial.data, status= status.HTTP_200_OK)


    def delete(self, request):
        if request.data:
            id = request.data['id']
            obj = self.get_object(id)
            obj.delete()
            return Response("Deleted successfully", status= status.HTTP_200_OK)
        


class booking(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = bookings.objects.all()
    serializer_class = bookingserializer


    def get(self, request):
        set = bookings.objects.all() 
        serial = bookingserializer(set, many=True)
        return Response(serial.data, status= status.HTTP_200_OK)

    
    def put(sef, request):
        try:
            id = request.data['id']
            obj = bookings.objects.get(id=id)
        except:
            return Response("obj not found", status= status.HTTP_400_BAD_REQUEST)
        serial = bookingserializer(obj, data= request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.data, status= status.HTTP_200_OK)
    
    def delete(self, request):
        if request.data:
            id = request.data['id']
            obj = bookings.objects.get(id = id)
            obj.delete()
            return Response('Deleted Successfully', status= status.HTTP_200_OK)





