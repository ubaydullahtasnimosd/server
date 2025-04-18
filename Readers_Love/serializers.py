from rest_framework import serializers
from .models import Readers_Love

class ReadersLoveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readers_Love
        fields = ['readersBookName', 'readersName', 'readersReview', 'readersReviewCreated']

class ReadersLoveImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readers_Love
        fields = ['readersBookImg', 'readersReviewCreated']