from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Visitor

class VisitorCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        visitor, created = Visitor.objects.get_or_create(id=1)
        return Response({'count': visitor.count}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        visitor, created = Visitor.objects.get_or_create(id=1)
        visitor.count += 1
        visitor.save()
        return Response({'message': 'Visitor count incremented', 'count': visitor.count}, status=status.HTTP_201_CREATED)