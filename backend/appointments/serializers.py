from xml.dom import ValidationErr
import datetime
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Appointment
from users.models import User
from place.models import Place
from users.serializers import UserSerializer
from place.serializers import PlaceSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(required=False, allow_blank=True)
    subject = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(required=False, default=timezone.now())
    time = serializers.TimeField(required=False, default=datetime.time(0, 0))
    offline_mode = serializers.BooleanField(default=True, required=False)
    meeting_link = serializers.CharField(required=False)
    host_username = serializers.CharField(required=False)
    place_name = serializers.CharField(required=False)

    class Meta:
        model = Appointment
        fields = (
            "topic",
            "subject",
            "description",
            "date",
            "time",
            "offline_mode",
            "meeting_link",
            "host_username",
            "place_name",
        )


class AppointmentCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        print('asdsadasda')
        print(data)
        user = User.objects.filter(Q(username=data['host_username']))
        place_name = data['place_name']
        if not user.exists():
            raise ValidationError("username is not found.")
        user = User.objects.get(username=data['host_username'])
        Appointment.objects.create(
            topic=data['topic'],
            subject=data['subject'],
            description='description',
            date=timezone.now(),
            time=datetime.time(0, 0),
            offline_mode=True,
            meeting_link='',
            host_username=data['host_username'],
            host=user,
            place_name=place_name,
        )
        return data

    class Meta:
        model = Appointment
        fields = (
            "topic",
            "subject",
            "description",
            "date",
            "time",
            "offline_mode",
            "meeting_link",
            "host_username",
            "place_name",
        )


class AppointmentJoinSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    appointment_id = serializers.IntegerField()

    def validate(self, data):
        print(data)
        user = User.objects.filter(Q(username=data['username']))
        appointment = Appointment.objects.filter(Q(id=data['appointment_id']))
        if not user.exists():
            raise ValidationError("username is not found.")
        if not appointment.exists():
            raise ValidationError("appointment is not found.")
        return data

    class Meta:
        model = Appointment
        fields = ("username", "appointment_id")


class AppointmentsGetFilteredSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(allow_blank=True)
    topic = serializers.CharField(allow_blank=True)
    username = serializers.CharField(allow_blank=True)

    def validate(self, data):
        print(data)
        return data

    class Meta:
        model = Appointment
        fields = ('subject', 'topic', 'username')
