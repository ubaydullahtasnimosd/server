from rest_framework import serializers
from .models import Subscriber
import uuid

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'name', 'email', 'is_verified', 'subscribed_at']
        read_only_fields = ['id', 'is_verified', 'subscribed_at']

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']

    def create(self, validated_data):
        verification_token = str(uuid.uuid4())

        subscriber = Subscriber.objects.create(
            name = validated_data['name'],
            email = validated_data['email'],
            verification_token = verification_token,
        )

        subscriber.send_verification_email()

        return subscriber