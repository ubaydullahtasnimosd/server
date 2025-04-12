from rest_framework import generics
from .models import Articles_Essays
from .serializers import ArticlesEssaysSerializers

class ArticlesEssaysListCreateView(generics.ListCreateAPIView):
    queryset = Articles_Essays.objects.all()
    serializer_class = ArticlesEssaysSerializers
    
class ArticlesEssaysRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articles_Essays.objects.all()
    serializer_class = ArticlesEssaysSerializers
    lookup_field = 'id'