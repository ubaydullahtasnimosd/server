from rest_framework import generics
from .serializers import ReadersLoveListSerializer, ReadersLoveImageSerializer
from .models import Readers_Love

class ReadersLoveListView(generics.ListCreateAPIView):
    queryset = Readers_Love.objects.all()
    serializer_class = ReadersLoveListSerializer

class ReadersLoveImageView(generics.ListCreateAPIView):
    queryset = Readers_Love.objects.all()
    serializer_class = ReadersLoveImageSerializer