from rest_framework import serializers
from .models import Misecllaneous

class MisecllaneousSerializers(serializers.ModelSerializer):
    class Meta:
        model = Misecllaneous
        fields = ['misecllaneousTitle', 'misecllaneousVideo', 'misecllaneousCreateAt']