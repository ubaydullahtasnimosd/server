from rest_framework import serializers
from .models import Articles_Essays

class ArticlesEssaysSerializers(serializers.ModelSerializer):
    class Meta:
        model = Articles_Essays
        fields = ['id', 'articlesEssaysImg', 'articlesEssaysName', 'articlesEssaysAuthor', 'articlesEssaysDescription', 'articlesEssaysQRCodeScen', 'articlesEssaysQRCodeScenImg', 'articlesEssaysCreateAt', 'articlesEssaysUpdateAt']
        