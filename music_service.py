import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class MusicDataService:
    """Service to fetch music data from various APIs"""
    
    def __init__(self):
        # Initialize Spotify client
        self.spotify = None
        self._setup_spotify()
    
    def _setup_spotify(self):
        """Setup Spotify client with credentials"""
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
            )
            self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        except Exception as e:
            print(f"Error setting up Spotify: {e}")
            self.spotify = None
    
    def get_trending_songs(self, limit=10, country='US'):
        """Get trending songs from Spotify charts"""
        try:
            if not self.spotify:
                return self._get_mock_trending_songs(limit)
            
            # Get current trending playlists
            playlists = self.spotify.featured_playlists(country=country, limit=1)
            
            if playlists['playlists']['items']:
                playlist_id = playlists['playlists']['items'][0]['id']
                tracks = self.spotify.playlist_tracks(playlist_id, limit=limit)
                
                trending_songs = []
                for idx, item in enumerate(tracks['items']):
                    track = item['track']
                    song_info = {
                        'rank': idx + 1,
                        'title': track['name'],
                        'artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'album': track['album']['name'],
                        'release_date': track['album']['release_date'],
                        'duration_ms': track['duration_ms'],
                        'popularity': track['popularity'],
                        'spotify_url': track['external_urls']['spotify'],
                        'preview_url': track['preview_url']
                    }
                    trending_songs.append(song_info)
                
                return trending_songs
            else:
                return self._get_mock_trending_songs(limit)
                
        except Exception as e:
            print(f"Error fetching trending songs: {e}")
            return self._get_mock_trending_songs(limit)
    
    def _get_mock_trending_songs(self, limit=10):
        """Mock trending songs data when API is not available"""
        mock_songs = [
            {
                'rank': 1,
                'title': 'Flowers',
                'artist': 'Miley Cyrus',
                'album': 'Endless Summer Vacation',
                'release_date': '2023-01-13',
                'duration_ms': 200000,
                'popularity': 95,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 2,
                'title': 'Anti-Hero',
                'artist': 'Taylor Swift',
                'album': 'Midnights',
                'release_date': '2022-10-21',
                'duration_ms': 201000,
                'popularity': 94,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 3,
                'title': 'Unholy',
                'artist': 'Sam Smith, Kim Petras',
                'album': 'Unholy',
                'release_date': '2022-09-22',
                'duration_ms': 156000,
                'popularity': 92,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 4,
                'title': 'As It Was',
                'artist': 'Harry Styles',
                'album': 'Harry\'s House',
                'release_date': '2022-04-01',
                'duration_ms': 167000,
                'popularity': 91,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 5,
                'title': 'Watermelon Sugar',
                'artist': 'Harry Styles',
                'album': 'Fine Line',
                'release_date': '2019-12-13',
                'duration_ms': 174000,
                'popularity': 89,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 6,
                'title': 'Blinding Lights',
                'artist': 'The Weeknd',
                'album': 'After Hours',
                'release_date': '2019-11-29',
                'duration_ms': 200000,
                'popularity': 88,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 7,
                'title': 'Good 4 U',
                'artist': 'Olivia Rodrigo',
                'album': 'SOUR',
                'release_date': '2021-05-14',
                'duration_ms': 178000,
                'popularity': 87,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 8,
                'title': 'Levitating',
                'artist': 'Dua Lipa',
                'album': 'Future Nostalgia',
                'release_date': '2020-03-27',
                'duration_ms': 203000,
                'popularity': 86,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 9,
                'title': 'Stay',
                'artist': 'The Kid LAROI, Justin Bieber',
                'album': 'Stay',
                'release_date': '2021-07-09',
                'duration_ms': 141000,
                'popularity': 85,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            },
            {
                'rank': 10,
                'title': 'Heat Waves',
                'artist': 'Glass Animals',
                'album': 'Dreamland',
                'release_date': '2020-06-29',
                'duration_ms': 238000,
                'popularity': 84,
                'spotify_url': 'https://open.spotify.com/track/mock',
                'preview_url': None
            }
        ]
        return mock_songs[:limit]
    
    def search_song(self, query, limit=5):
        """Search for songs by query"""
        try:
            if not self.spotify:
                return []
            
            results = self.spotify.search(q=query, type='track', limit=limit)
            songs = []
            
            for track in results['tracks']['items']:
                song_info = {
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'release_date': track['album']['release_date'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity'],
                    'spotify_url': track['external_urls']['spotify'],
                    'preview_url': track['preview_url']
                }
                songs.append(song_info)
            
            return songs
            
        except Exception as e:
            print(f"Error searching songs: {e}")
            return []
    
    def get_artist_info(self, artist_name):
        """Get detailed information about an artist"""
        try:
            if not self.spotify:
                return self._get_mock_artist_info(artist_name)
            
            results = self.spotify.search(q=artist_name, type='artist', limit=1)
            
            if results['artists']['items']:
                artist = results['artists']['items'][0]
                
                # Get top tracks
                top_tracks = self.spotify.artist_top_tracks(artist['id'])
                
                # Get albums
                albums = self.spotify.artist_albums(artist['id'], album_type='album', limit=5)
                
                artist_info = {
                    'name': artist['name'],
                    'followers': artist['followers']['total'],
                    'popularity': artist['popularity'],
                    'genres': artist['genres'],
                    'spotify_url': artist['external_urls']['spotify'],
                    'images': artist['images'],
                    'top_tracks': [
                        {
                            'name': track['name'],
                            'album': track['album']['name'],
                            'popularity': track['popularity']
                        } for track in top_tracks['tracks'][:5]
                    ],
                    'albums': [
                        {
                            'name': album['name'],
                            'release_date': album['release_date'],
                            'total_tracks': album['total_tracks']
                        } for album in albums['items']
                    ]
                }
                
                return artist_info
            else:
                return self._get_mock_artist_info(artist_name)
                
        except Exception as e:
            print(f"Error getting artist info: {e}")
            return self._get_mock_artist_info(artist_name)
    
    def _get_mock_artist_info(self, artist_name):
        """Mock artist info when API is not available"""
        return {
            'name': artist_name,
            'followers': 1000000,
            'popularity': 85,
            'genres': ['pop', 'rock'],
            'spotify_url': 'https://open.spotify.com/artist/mock',
            'images': [],
            'top_tracks': [
                {'name': 'Popular Song 1', 'album': 'Latest Album', 'popularity': 90},
                {'name': 'Popular Song 2', 'album': 'Previous Album', 'popularity': 85}
            ],
            'albums': [
                {'name': 'Latest Album', 'release_date': '2023-01-01', 'total_tracks': 12}
            ]
        }


class LyricsService:
    """Service to fetch lyrics from various sources"""
    
    def __init__(self):
        self.genius_token = os.getenv('GENIUS_ACCESS_TOKEN')
    
    def get_lyrics(self, song_title, artist_name):
        """Get lyrics for a song"""
        try:
            if self.genius_token:
                return self._get_lyrics_from_genius(song_title, artist_name)
            else:
                return self._get_mock_lyrics(song_title, artist_name)
        except Exception as e:
            print(f"Error fetching lyrics: {e}")
            return self._get_mock_lyrics(song_title, artist_name)
    
    def _get_lyrics_from_genius(self, song_title, artist_name):
        """Fetch lyrics from Genius API"""
        try:
            import lyricsgenius
            genius = lyricsgenius.Genius(self.genius_token)
            genius.verbose = False
            genius.remove_section_headers = True
            
            song = genius.search_song(song_title, artist_name)
            
            if song:
                return {
                    'title': song.title,
                    'artist': song.artist,
                    'lyrics': song.lyrics,
                    'url': song.url
                }
            else:
                return self._get_mock_lyrics(song_title, artist_name)
                
        except Exception as e:
            print(f"Error with Genius API: {e}")
            return self._get_mock_lyrics(song_title, artist_name)
    
    def _get_mock_lyrics(self, song_title, artist_name):
        """Mock lyrics when API is not available"""
        return {
            'title': song_title,
            'artist': artist_name,
            'lyrics': f"[Lyrics for '{song_title}' by {artist_name} would appear here]\n\n[This is a demo version - please configure your Genius API key to get actual lyrics]",
            'url': 'https://genius.com/mock-url'
        }
