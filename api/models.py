from django.db import models
from django.contrib.auth.models import User
from django_unique_slugify import unique_slugify
from api.constants import ARTIST_CHOICES, GENRE_CHOICES

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.TextField(max_length=1200)
    type = models.CharField(max_length=10, choices=ARTIST_CHOICES)
    description = models.TextField(max_length=1200)
    birth = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Artist, self).save(*args, **kwargs)


class MusicVideo(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    release_year = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    image = models.TextField(max_length=1200)
    yt_embedded = models.CharField(max_length=255)
    rate_score = models.DecimalField(decimal_places=1, max_digits=2, default=0)
    votes_number = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=255)
    genre = models.CharField(
        max_length=50, choices=GENRE_CHOICES, default=None, null=True)
    song_description = models.TextField(max_length=1200, default='No info')

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title+'-'+self.album)
        super(MusicVideo, self).save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    musicVideo = models.ForeignKey(MusicVideo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()


class UserVideoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    musicVideos = models.ManyToManyField(MusicVideo)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super(UserVideoList, self).save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    musicVideo = models.ForeignKey(MusicVideo, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1200)