from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Subscriber
from .serializers import SubscriberSerializer, SubscribeSerializer
from django.shortcuts import get_object_or_404

class SubscribeView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscribeSerializer

class VerifySubscriptionView(APIView):
    def get(self, request, token, *args, **kwargs):
        subscriber = get_object_or_404(Subscriber, verification_token=token)

        if not subscriber.is_verified:
            subscriber.is_verified = True
            subscriber.save()
            subscriber.send_welcome_email()
            return Response({"Message" : "সাবস্ক্রিপশন সফলভাবে নিশ্চিত করা হয়েছে!"}, status=status.HTTP_200_OK)
        return Response({"Message" : "এই সাবস্ক্রিপশন ইতিমধ্যেই নিশ্চিত করা হয়েছে"}, status=status.HTTP_200_OK)
    
class SubscriberListView(generics.ListAPIView):
    queryset = Subscriber.objects.filter(is_verified=True)
    serializer_class = SubscriberSerializer