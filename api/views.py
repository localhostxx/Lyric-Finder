
from pandas.io.parsers import read_csv

from .models import Lyrics
from django.shortcuts import render


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import LyricsSerializer, SearchSerializer
from .models import Lyrics

from .docuSim import *
from django.contrib.staticfiles import finders


# Create your views here.


@api_view(['GET'])
def lyric(request):
    tasks = Lyrics.objects.all()
    serializer = LyricsSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def search(request):
    print(request)
    tasks = Lyrics.objects.all()
    if tasks is not None:
        tasks.delete()
    serializer = SearchSerializer(data=request.data)
    if serializer.is_valid():
        keyword = serializer.validated_data['keyword']
        if len(keyword) != 0:
            lyrics_loc = "data\lyrics.csv"
            data_path = finders.find(lyrics_loc)
            print(data_path)
            searc_loc = finders.searched_locations
            print("Locations: %s" % searc_loc)
            if len(searc_loc) > 0:
                lyrics_path = "%s\%s" % (
                    searc_loc[0], lyrics_loc)
                print(lyrics_path)
                dataframe = read_csv(lyrics_path)
                lyrics_ids = tfidf(keyword, lyrics_path)
                print(lyrics_ids)
            for lyric in lyrics_ids:
                context = {
                    "artist": dataframe.loc[lyric, 'Artist Name'],
                    "song": dataframe.loc[lyric, 'Song Name'],
                    "lyrics": dataframe.loc[lyric, 'Lyrics']
                }

                print(context)

                serializer = LyricsSerializer(data=context)
                if serializer.is_valid():
                    serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def detail(request, pk):
    tasks = Lyrics.objects.get(id=pk)
    serializer = LyricsSerializer(tasks, many=False)
    return Response(serializer.data)
