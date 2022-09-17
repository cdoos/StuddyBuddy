from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Appointment
from users.models import User
from .serializers import AppointmentSerializer, AppointmentCreateSerializer, AppointmentJoinSerializer, AppointmentsGetFilteredSerializer


class Create(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = AppointmentCreateSerializer(data=request.data)
        print(request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Join(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentJoinSerializer

    def join_appointment(self, appointment_id, username):
        user = User.objects.get(username=username)
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.users.add(user)
        return {
            "username": username,
            "appointment_id": appointment_id,
        }

    def post(self, request, *args, **kwargs):
        serializer_class = AppointmentJoinSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(self.join_appointment(request.data["appointment_id"], request.data["username"]), status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class GetFiltered(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AppointmentsGetFilteredSerializer

    def get_appointments(self, data):
        appointments = []
        username = data['username']
        if username == '':
            for app in Appointment.objects.all():
                appointments.append(app)
        else:
            all_appointments = Appointment.objects.all()
            for app in all_appointments:
                if app.users.filter(username=username).count() == 0 and app.host.username != username:
                    appointments.append(app)
        filtered_appointments = []
        for appointment in appointments:
            appointment_users = []
            for user in appointment.users.all():
                appointment_users.append(user.username)
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
            filtered_appointments.append(appointment_info)
        return filtered_appointments

    def post(self, request, *args, **kwargs):
        serializer_class = AppointmentsGetFilteredSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(self.get_appointments(request.data), status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
