from rest_framework import serializers
from .models import Culture, History, Misecllaneous, Politics, Travel, Worldview

class MisecllaneousSerializers(serializers.ModelSerializer):
    class Meta:
        model = Misecllaneous
        fields = ['misecllaneousTitle', 'misecllaneousVideo', 'misecllaneousCreateAt']


class MiscellaneousContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "contentImg",
            "contentName",
            "contentAuthor",
            "contentDescription",
            "contentCreateAt",
            "contentUpdateAt",
        ]
        read_only_fields = ["id", "contentCreateAt", "contentUpdateAt"]


class CultureSerializer(MiscellaneousContentSerializer):
    class Meta(MiscellaneousContentSerializer.Meta):
        model = Culture


class TravelSerializer(MiscellaneousContentSerializer):
    class Meta(MiscellaneousContentSerializer.Meta):
        model = Travel


class HistorySerializer(MiscellaneousContentSerializer):
    class Meta(MiscellaneousContentSerializer.Meta):
        model = History


class PoliticsSerializer(MiscellaneousContentSerializer):
    class Meta(MiscellaneousContentSerializer.Meta):
        model = Politics


class WorldviewSerializer(MiscellaneousContentSerializer):
    class Meta(MiscellaneousContentSerializer.Meta):
        model = Worldview
