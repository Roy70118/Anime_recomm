from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import requests
import logging
import aiohttp
# Setup AniList GraphQL client
transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
client = Client(transport=transport, fetch_schema_from_transport=True)

# Fetch anime by name or genre


async def search_anime(query, genre=None):
    query_string = gql("""
    query ($search: String, $genre: String) {
        Page(page: 1, perPage: 10) {
            media(search: $search, genre_in: [$genre], type: ANIME) {
                id
                title {
                    romaji
                    english
                }
                genres
                averageScore
                description
                coverImage {
                    large
                }
            }
        }
    }
    """)
    variables = {"search": query, "genre": genre}
    async with client as session:
        response = await session.execute(query_string, variable_values=variables)
    return response["Page"]["media"]

# Fetch recommended anime


# async def recommend_anime(user_genres):
#     query_string = gql("""
#     query ($genres: [String]) {
#         Page(page: 1, perPage: 10) {
#             media(genre_in: $genres, sort: POPULARITY_DESC, type: ANIME) {
#                 id
#                 title {
#                     romaji
#                     english
#                 }
#                 genres
#                 averageScore
#                 description
#                 coverImage {
#                     large
#                 }
#             }
#         }
#     }
#     """)
#     variables = {"genres": user_genres}
#     async with client as session:
#         response = await session.execute(query_string, variable_values=variables)
#     return response["Page"]["media"]


# Fetch recommended anime
async def fetch_anime_recommendations_async(genres, watched_anime, user_token):
    query = """
    query ($genres: [String], $exclude: [String]) {
        Page {
            media(genre_in: $genres, title_not_in: $exclude, type: ANIME) {
                id
                title {
                    english
                }
                genres
            }
        }
    }
    """
    variables = {
        "genres": genres,
        "exclude": watched_anime
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token}"  # Use real token here
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://graphql.anilist.co/', json={'query': query, 'variables': variables}, headers=headers) as response:
            response_data = await response.json()

            if response.status != 200:
                logging.error(
                    f"Error fetching recommendations: {response_data}")
                return None

            return response_data.get('data', {}).get('Page', {}).get('media', [])
