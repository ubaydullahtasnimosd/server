from rest_framework import generics
from .models import Misecllaneous
from .serializers import MisecllaneousSerializers

class MisecllaneousApiView(generics.ListCreateAPIView):
    queryset = Misecllaneous.objects.all()
    serializer_class = MisecllaneousSerializers