from rest_framework import serializers, validators
from .models import Artist, Rating, MusicVideo, UserVideoList
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token['username'] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

        extra_kwargs = {
            'password': {"write_only": True},
            'email': {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already exists"
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('artist_id', 'name', 'image', 'type',
                  'description', 'birth', 'slug')

    def create(self, validated_data):
        print('validated_data: ', validated_data)
        artist = super().create(validated_data)
        artist.save()
        return artist


class MusicVideoSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = MusicVideo
        fields = ('id', 'artist', 'title', 'slug', 'release_year', 'album', 'image',
                  'yt_embedded', 'rate_score', 'votes_number', 'duration', 'genre')

    def create(self, validated_data):
        validated_data['artist'] = Artist.objects.get(
            artist_id=self.context['artist'])
        return super().create(validated_data)


class RatingSerializer(serializers.ModelSerializer):
    musicVideo = MusicVideoSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'rating', 'date', 'musicVideo',
                  'user')

        extra_kwargs = {
            'rating': {"required": True},
        }

    def create(self, validated_data):
        validated_data['musicVideo'] = MusicVideo.objects.get(id=self.context['musicVideo_id'])
        return super().create(validated_data)


class UserVideoListSerializer(serializers.ModelSerializer):
    musicVideos = MusicVideoSerializer(many=True)

    class Meta:
        model = UserVideoList
        fields = '__all__'

class UserVideoListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideoList
        fields = '__all__'