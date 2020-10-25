from django.db.models import fields
from rest_framework import serializers
from .models import Lyrics, Search


class LyricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyrics
        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
