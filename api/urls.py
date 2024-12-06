from django.urls import path, include
from api.views import *
# from api.views import UserRegistrationView
urlpatterns = [
    path("auth/register/", UserRegistrationView.as_view(), name='register'),
    path("auth/login/", UserLoginView.as_view(), name='login'),
    path("anime/search/", AnimeSearchView.as_view(), name="anime-search"),
    path("anime/recommendation/", AnimeRecommendationView.as_view(),
         name="anime-recommend"),
    path("user/preferences/", UserPreferencesView.as_view(), name="user-preferences")
]
