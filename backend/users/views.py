from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
import requests
from .models import User
from appointments.models import Appointment
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, UserGetAppointmentsSerializer


class Register(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class GetAppointments(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetAppointmentsSerializer

    def get_appointments(self, username: str):
        user = User.objects.get(username=username)
        appointments = Appointment.objects.all()
        user_appointments = []
        for appointment in appointments:
            appointment_users = []
            okay = False
            for user in appointment.users.all():
                if user.username == username:
                    okay = True
                    break
            if appointment.host.username == username:
                okay = True

            if okay == False:
                continue
            appointment_info = {
                "id": appointment.id,
                "topic": appointment.topic,
                "subject": appointment.subject,
                "description": appointment.description,
                "date": appointment.date,
                "time": appointment.time,
                "offline_mode": appointment.offline_mode,
                "meeting_link": appointment.meeting_link,
                "host_username": appointment.host.username,
                "place_name": appointment.place_name,
                "users": appointment_users,
                "host": {
                    "username": appointment.host.username,
                },
            }
            user_appointments.append(appointment_info)
        return user_appointments

    def post(self, request, *args, **kwargs):
        serializer_class = UserGetAppointmentsSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(self.get_appointments(request.data["username"]), status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class GetAppointmentsNumber(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetAppointmentsSerializer

    def get_appointments_number(self, username: str):
        user = User.objects.get(username=username)
        return user.appointments.all().count()

    def post(self, request, *args, **kwargs):
        serializer_class = UserGetAppointmentsSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(self.get_appointments_number(request.data["username"]), status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class MatchUser(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetAppointmentsSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer_class = UserGetAppointmentsSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            user = User.objects.get(username=request.data['username'])
            url = 'http://0.0.0.0:8008'
            body = {
                'id': user.id,
                'good': user.good,
                'bad': user.bad
            }
            requests.post(url=url + '/add/', json=body)
            response = requests.get(url='{}/find/{}/1/'.format(url, user.id))
            data = response.json()
            if response.status_code == 404 or len(data) == 0:
                return Response('The match for user didn\'t found', status=HTTP_404_NOT_FOUND)
            if not data['Matches']:
                return Response('The matched user didn\'t found', status=HTTP_404_NOT_FOUND)
            matched_user = User.objects.get(id=data['Matches'][0])
            response_body = {'username': matched_user.username,
                             'good': matched_user.good,
                             'bad': matched_user.bad}
            return Response(response_body, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
