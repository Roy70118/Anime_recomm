Anime Search and Recommendation System

Project Overview:
The Anime Search and Recommendation System is a backend application built using Django REST Framework and the AniList GraphQL API. It allows users to search for anime by name or genre and fetch anime recommendations based on their preferences, such as favorite genres or watched anime. The system uses PostgreSQL to store user data and preferences and implements JWT-based authentication to secure access to user-specific endpoints.
Features

    Anime Search: Search for anime by name or genre using the AniList GraphQL API.
    Recommendations: Fetch personalized anime recommendations based on user preferences (e.g., favorite genres or watched anime).
    User Authentication: Secure login and registration with JWT token-based authentication.
    User Preferences: Manage and update user preferences, including favorite genres and watched anime.
    Database: Store user credentials, preferences, and optionally, cached anime data for better performance.

Tech Stack

    Backend: Django REST Framework
    Database: PostgreSQL
    Authentication: JWT
    External API: AniList GraphQL API
    Environment: Python 3.x

Installation
Prerequisites

Ensure you have the following installed:

    Python 3.x
    PostgreSQL

Clone the Repository

git clone https://github.com/your-username/anime-recommendation-system.git
cd anime-recommendation-system

Install Dependencies

Create and activate a virtual environment, then install the necessary dependencies:

# Create virtual environment (optional)
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate


# Install dependencies
pip install -r requirements.txt

Set Up Database

    Create a PostgreSQL database.
    Update the DATABASES setting in settings.py with your database credentials.
    Run migrations to set up the database schema:

python manage.py migrate

Run the Development Server

Start the Django development server:

python manage.py runserver

The application should now be running on http://127.0.0.1:8000/.
API Testing with Postman

 I am used  Postman to test the API endpoints. Below are the available endpoints:

    User Registration:
        POST /auth/register
        Request Body: { "username": "user", "password": "password", "email": "user@example.com" }

    User Login:
        POST /auth/login
        Request Body: { "username": "user", "password": "password" }

    Anime Search:
        GET /anime/search?query=anime_name
        Query Params: query (Anime name or genre)

    Anime Recommendations:
        GET /anime/recommendations
        Headers: { "Authorization": "Bearer <JWT_Token>" }

    User Preferences:
        GET /user/preferences
        Headers: { "Authorization": "Bearer <JWT_Token>" }
        Request Body: { "favorite_genres": ["action", "adventure"] }

