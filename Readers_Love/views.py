from rest_framework import generics
from .serializers import ReadersLoveSerializers
from .models import Readers_Love

class ReadersLoveApiView(generics.ListCreateAPIView):
    queryset = Readers_Love.objects.all()
    serializer_class = ReadersLoveSerializers