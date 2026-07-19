from rest_framework import generics
from .models import Culture, History, Misecllaneous, Politics, Travel, Worldview
from .serializers import (
    CultureSerializer,
    HistorySerializer,
    MisecllaneousSerializers,
    PoliticsSerializer,
    TravelSerializer,
    WorldviewSerializer,
)

class MisecllaneousApiView(generics.ListCreateAPIView):
    queryset = Misecllaneous.objects.all()
    serializer_class = MisecllaneousSerializers


class CultureListCreateView(generics.ListCreateAPIView):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer


class CultureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer
    lookup_field = "id"


class TravelListCreateView(generics.ListCreateAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer


class TravelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer
    lookup_field = "id"


class HistoryListCreateView(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer


class HistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    lookup_field = "id"


class PoliticsListCreateView(generics.ListCreateAPIView):
    queryset = Politics.objects.all()
    serializer_class = PoliticsSerializer


class PoliticsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Politics.objects.all()
    serializer_class = PoliticsSerializer
    lookup_field = "id"


class WorldviewListCreateView(generics.ListCreateAPIView):
    queryset = Worldview.objects.all()
    serializer_class = WorldviewSerializer


class WorldviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worldview.objects.all()
    serializer_class = WorldviewSerializer
    lookup_field = "id"
