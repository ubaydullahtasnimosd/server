from rest_framework import serializers
from .models import AboutAuthor

class AboutAuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = AboutAuthor
        fields = ['aboutAuthorImg', 'aboutAuthorName', 'aboutAuthorDescription']