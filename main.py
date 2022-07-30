import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = input("Client ID: ")
CLIENT_SECRET = input("Client Secret: ")
REDIRECT_URI = input("redirect_uri: ")
USERNAME = input("Spotify Username: ")


class TopSongs:
    """Create a Spotify playlist of top 100 songs on the user inputted date."""
    def __init__(self):
        # Ask the user the date they want to travel.
        self.travel_date = input("Which date do you want to travel to? Type in YYYY-MM-DD format: ")
        self.run_the_program()

    def run_the_program(self):
        # Get names of top 100 hits on that date as a list.
        top_100_hits = self.get_top_hits()
        # Create a spotify playlist including all 100 songs.
        self.create_the_playlist(top_100_hits)

    def get_top_hits(self) -> list:
        """Get top 100 hits on that given date."""
        URL = f"https://www.billboard.com/charts/hot-100/{self.travel_date}/"
        response = requests.get(URL)
        website_html = response.text
        soup = BeautifulSoup(website_html, "html.parser")

        all_song_details = soup.select(selector=".chart-results-list #title-of-a-story")
        all_song_details_stripped = [item.getText().strip() for item in all_song_details]
        all_top_song_names = all_song_details_stripped[2::4]
        return all_top_song_names

    def create_the_playlist(self, song_names: list):
        """Create the spotify playlist to the given songs list"""
        scope = "playlist-modify-public"

        token = SpotifyOAuth(scope=scope, username=USERNAME)
        spotify_object = spotipy.Spotify(auth_manager=token)

        # Create playlist.
        playlist_name = f"Top 100 songs on {self.travel_date}"
        playlist_description = f"These are the top 100 songs on {self.travel_date}. Hope you enjoy!"
        spotify_object.user_playlist_create(user=USERNAME, name=playlist_name, public=True,
                                            description=playlist_description)

        # Get URIs for the songs.
        list_of_song_uris = []
        for song_name in song_names:
            song_result = spotify_object.search(q=song_name, limit=1)
            list_of_song_uris.append(song_result["tracks"]["items"][0]["uri"])

        # Get the relevant playlist.
        pre_playlist = spotify_object.user_playlists(user=USERNAME)
        playlist = pre_playlist["items"][0]["id"]

        # Add songs to the playlist.
        spotify_object.user_playlist_add_tracks(user=USERNAME, playlist_id=playlist, tracks=list_of_song_uris)


if __name__ == "__main__":
    playlist = TopSongs()