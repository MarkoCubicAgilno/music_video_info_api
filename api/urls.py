from django.urls import path
from .views import ArtistView, RegisterView, RatingListView, MusicVideoView, SearchView, UserVideoListView, VideographyView
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('artist/', ArtistView.as_view()),
    path('artist/<slug:slug>/', ArtistView.as_view()),
    path('rating/', RatingListView.as_view()),
    path('rating-update/<int:pk>/', RatingListView.as_view()),
    path('rating/<int:user_id>/', RatingListView.as_view()),
    path('rating/<int:user_id>/<slug:musicVideo_slug>/', RatingListView.as_view()),
    path('music-video/', MusicVideoView.as_view()),
    path('music-video/<slug:slug>/', MusicVideoView.as_view()),
    path('video-lists/', UserVideoListView.as_view()),
    path('video-lists/<int:user_id>/', UserVideoListView.as_view()),
    path('video-lists/<slug:slug>/', UserVideoListView.as_view()),
    path('video-lists/<slug:slug>/<int:music_video_id>/', UserVideoListView.as_view()),
    path('search/', SearchView.as_view()),
    path('videography/<slug:slug>/', VideographyView.as_view()),
]
