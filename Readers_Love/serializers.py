from rest_framework import serializers
from .models import Readers_Love

class ReadersLoveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Readers_Love
        fields = ['readersBookImg', 'readersBookName', 'readersName', 'readersReview', 'readersReviewCreated']