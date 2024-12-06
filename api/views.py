import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.serializers import *
from api.helpers import *
from api.models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import asyncio
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request,  format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Sucessful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'erros': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

# Add views for the search and recommendation features


class AnimeSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("query", "")
        genre = request.query_params.get("genre", None)
        if not query:
            return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Perform the search using the AniList API
            result = asyncio.run(search_anime(query, genre))
            return Response({"results": result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class AnimeSearchView(APIView):
    # permission_classes = [AllowAny]

    # def get(self, request):
    #     query = request.query_params.get("query", "").strip()
    #     genre = request.query_params.get("genre", "").strip()

    #     if not query:
    #         return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     # AniList GraphQL API endpoint
    #     url = "https://graphql.anilist.co"

    #     # GraphQL query
    #     gql_query = """
    #     query ($search: String, $genre: String) {
    #         Page {
    #             media(search: $search, genre_in: [$genre], type: ANIME) {
    #                 id
    #                 title {
    #                     romaji
    #                     english
    #                 }
    #                 genres
    #                 popularity
    #             }
    #         }
    #     }
    #     """

    #     # GraphQL variables
    #     variables = {"search": query}
    #     if genre:
    #         variables["genre"] = genre

    #     # Make the request to AniList API
    #     try:
    #         response = requests.post(
    #             url,
    #             json={"query": gql_query, "variables": variables},
    #             headers={"Content-Type": "application/json"},
    #         )
    #         if response.status_code == 200:
    #             return Response(response.json(), status=status.HTTP_200_OK)
    #         else:
    #             return Response(
    #                 {"error": f"AniList API error: {response.status_code}"},
    #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             )
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AnimeRecommendationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_preferences = UserPreferences.objects.filter(
            user=request.user).first()

        if not user_preferences:
            return Response({"error": "User preferences not found."}, status=404)

        genres = user_preferences.genres
        watched_anime = user_preferences.watched_anime

        if not genres:
            return Response({"error": "Genres not set in preferences."}, status=400)

        # Extract JWT token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed("Authorization header missing")

        try:
            # Assuming the format is "Bearer <token>"
            token = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed("Invalid token format")

        # Fetch recommendations asynchronously using the token
        recommendations = asyncio.run(
            fetch_anime_recommendations_async(genres, watched_anime, token))

        if not recommendations:
            return Response({"error": "Failed to fetch recommendations."}, status=500)

        return Response({"recommendations": recommendations}, status=200)


class UserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch user preferences
        user_preferences = UserPreferences.objects.filter(
            user=request.user).first()

        if user_preferences:
            serializer = UserPreferencesSerializer(user_preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User preferences not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Create preferences if they don't exist
        if UserPreferences.objects.filter(user=request.user).exists():
            return Response({"error": "Preferences already exist. Use PATCH to update."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"msg": "Preferences created successfully", "preferences": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # Update preferences
        user_preferences = UserPreferences.objects.filter(
            user=request.user).first()
        if not user_preferences:
            return Response({"error": "User preferences not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserPreferencesSerializer(
            user_preferences, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Preferences updated successfully", "preferences": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
