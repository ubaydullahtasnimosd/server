from rest_framework import serializers
from .models import Readers_Love, Readers_Love_Img

class ReadersLoveImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readers_Love_Img
        fields = ['readersBookImg', 'readersReviewCreated']

class ReadersLoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readers_Love
        fields = ['readersBookName', 'readersName', 'readersReview', 'readersReviewCreated']