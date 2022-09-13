from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Artist, Rating, MusicVideo, Review, UserVideoList
from django.contrib.auth.models import User
from api.serializers import ArtistSerializer, MusicVideoSerializer, MyTokenObtainPairSerializer, ReviewSerializer, UserSerializer, RatingSerializer, UserVideoListCreateSerializer, UserVideoListSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import Http404
from django.db.models import Avg


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArtistView(APIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get(self, request, slug=None):
        if slug:
            try:
                artist = Artist.objects.get(slug=slug)
                serializer = self.serializer_class(artist)

            except Artist.DoesNotExist:
                return Response({'status': 'error', 'message': 'Artist does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)

        artists = Artist.objects.all()
        serializer = self.serializer_class(artists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingListView(APIView):
    def get_object(self, pk):
        try:
            return Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            raise Http404

    def get(self, request, user_id=None, musicVideo_slug=None, rating=None, order=None):
        if (user_id and musicVideo_slug):
            try:
                music_video = MusicVideo.objects.get(slug=musicVideo_slug)

            except MusicVideo.DoesNotExist:
                ratings = None
                return Response({'status': 'error', 'message': 'Music Video does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                ratings = Rating.objects.get(
                    musicVideo_id=music_video.id, user_id=user_id)
            except Rating.DoesNotExist:
                ratings = None
                return Response({'status': 'error', 'message': 'Rating does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = RatingSerializer(ratings)

        elif (user_id):
            ratings = Rating.objects.all().filter(user_id=user_id)
            if (rating):
                ratings = ratings.filter(rating=rating)
            if (order):
                if order == 'date':
                    ratings = ratings.order_by('-date')

                elif order == 'top':
                    ratings = ratings.order_by('-rating')

                serializer = RatingSerializer(ratings, many=True)

        else:
            ratings = Rating.objects.all()
            serializer = RatingSerializer(ratings, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = RatingSerializer(data=request.data, context={
                                      'musicVideo_id': request.data['musicVideo']})
        if serializer.is_valid():
            serializer.save()

            ratings = Rating.objects.filter(
                musicVideo_id=request.data['musicVideo']).aggregate(Avg('rating'))
            music_video = MusicVideo.objects.get(id=request.data['musicVideo'])
            music_video.votes_number = music_video.votes_number + 1
            music_video.rate_score = ratings['rating__avg']
            music_video.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        rating = self.get_object(pk)
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()

            ratings = Rating.objects.filter(
                musicVideo_id=rating.musicVideo.id).aggregate(Avg('rating'))
            music_video = MusicVideo.objects.get(id=rating.musicVideo.id)
            music_video.rate_score = ratings['rating__avg']
            music_video.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()

        ratings = Rating.objects.filter(
            musicVideo_id=snippet.musicVideo.id).aggregate(Avg('rating'))
        music_video = MusicVideo.objects.get(id=snippet.musicVideo.id)
        music_video.votes_number = music_video.votes_number - 1
        music_video.rate_score = ratings['rating__avg']
        music_video.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicVideoView(generics.ListAPIView):
    queryset = MusicVideo.objects.all()
    serializer_class = MusicVideoSerializer

    def get(self, request, slug=None):
        if slug:
            try:
                music_video = MusicVideo.objects.get(slug=slug)
                serializer = self.serializer_class(music_video)

            except MusicVideo.DoesNotExist:
                return Response({'status': 'error', 'message': 'Music Video does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)

        music_videos = MusicVideo.objects.all()
        serializer = self.serializer_class(music_videos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={
                                           'artist': request.data['artist']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):
        video = MusicVideo.objects.get(slug=slug)
        serializer = self.serializer_class(
            video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVideoListView(APIView):
    serializer_class = UserVideoListSerializer
    serializer_create_class = UserVideoListCreateSerializer

    def get(self, request, user_id=None, slug=None):
        if user_id:
            user_video_list = UserVideoList.objects.filter(user_id=user_id)
            serializer = self.serializer_class(user_video_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif slug:
            user_video_list = UserVideoList.objects.get(slug=slug)
            serializer = self.serializer_class(user_video_list)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, slug=None, music_video_id=None):
        if slug and music_video_id:
            user_list = UserVideoList.objects.get(slug=slug)
            music_video = MusicVideo.objects.get(id=music_video_id)
            user_list.musicVideos.add(music_video)
            return Response({'message': 'Successfully added music video to list'}, status=status.HTTP_201_CREATED)

        serializer = self.serializer_create_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):
        list = UserVideoList.objects.get(slug=slug)
        serializer = self.serializer_create_class(
            list, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, music_video_id=None):
        if music_video_id:
            user_list = UserVideoList.objects.get(slug=slug)
            music_video = MusicVideo.objects.get(id=music_video_id)
            user_list.musicVideos.remove(music_video)
            return Response({'message': 'removed selected video from list'}, status=status.HTTP_204_NO_CONTENT)

        snippet = UserVideoList.objects.get(slug=slug)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchMusicVideoView(APIView):
    def post(self, request):
        music_video = MusicVideo.objects.filter(
            title__icontains=request.data['parameter'])
        serializer = MusicVideoSerializer(music_video, many=True)

        return Response(serializer.data)


class SearchArtistView(APIView):
    def post(self, request):
        artist = Artist.objects.filter(
            name__icontains=request.data['parameter'])
        serializer = ArtistSerializer(artist, many=True)

        return Response(serializer.data)


class VideographyView(APIView):
    def get(self, request, slug=None):
        artist = Artist.objects.get(slug=slug)
        music_videos = MusicVideo.objects.filter(artist_id=artist.artist_id)
        serializer = MusicVideoSerializer(music_videos, many=True)

        return Response(serializer.data)


class ReviewView(APIView):
    reviews = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, slug=None):
        if slug:
            try:
                music_video = MusicVideo.objects.get(slug=slug)
                filtered_reviews = Review.objects.filter(
                    musicVideo_id=music_video.id)
                serializer = self.serializer_class(filtered_reviews, many=True)

            except MusicVideo.DoesNotExist:
                return Response({'status': 'error', 'message': 'Music Video does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.serializer_class(self.reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={
                                           'user': request.data['user']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        review = Review.objects.get(id=pk)
        serializer = self.serializer_class(
            review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
