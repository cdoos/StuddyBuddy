from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Place
from .serializers import PlaceSerializer


class Create(generics.ListCreateAPIView):
    # get method handler
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
