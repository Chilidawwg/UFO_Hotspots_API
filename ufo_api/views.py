from rest_framework import generics
from ufo_api.models import Sighting
from ufo_api.serializers import SightingSerializer


class UFOData(generics.ListCreateAPIView):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer


class UFODataDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer


