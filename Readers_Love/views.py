from rest_framework import generics
from .models import Readers_Love, Readers_Love_Img
from .serializers import ReadersLoveSerializer, ReadersLoveImgSerializer

class ReadersLoveListCreateView(generics.ListCreateAPIView):
    queryset = Readers_Love.objects.all().order_by('-readersReviewCreated')
    serializer_class = ReadersLoveSerializer

class ReadersLoveImgListView(generics.ListAPIView):
    queryset = Readers_Love_Img.objects.all().order_by('-readersReviewCreated')
    serializer_class = ReadersLoveImgSerializer