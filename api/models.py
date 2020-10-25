from django.db import models

# Create your models here.


class Lyrics(models.Model):
    artist = models.CharField(max_length=200)
    song = models.CharField(max_length=200)
    lyrics = models.CharField(max_length=2048)


class Search(models.Model):
    keyword = models.CharField(max_length=200)
