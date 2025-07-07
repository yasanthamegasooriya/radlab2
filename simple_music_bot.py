# Simple Music Chatbot Test
# This is a minimal version that works without external APIs for testing

import re
import json
import random
from datetime import datetime

class SimpleMusicBot:
    """A simple music chatbot that works without external APIs"""
    
    def __init__(self):
        self.conversation_history = []
        self.mock_data = self._load_mock_data()
    
    def _load_mock_data(self):
        """Load mock music data for testing"""
        return {
            'trending_songs': [
                {
                    'rank': 1,
                    'title': 'Anti-Hero',
                    'artist': 'Taylor Swift',
                    'album': 'Midnights',
                    'popularity': 95,
                    'genre': 'Pop'
                },
                {
                    'rank': 2,
                    'title': 'As It Was',
                    'artist': 'Harry Styles',
                    'album': 'Harry\'s House',
                    'popularity': 92,
                    'genre': 'Pop Rock'
                },
                {
                    'rank': 3,
                    'title': 'Heat Waves',
                    'artist': 'Glass Animals',
                    'album': 'Dreamland',
                    'popularity': 89,
                    'genre': 'Alternative'
                },
                {
                    'rank': 4,
                    'title': 'Flowers',
                    'artist': 'Miley Cyrus',
                    'album': 'Endless Summer Vacation',
                    'popularity': 87,
                    'genre': 'Pop'
                },
                {
                    'rank': 5,
                    'title': 'Unholy',
                    'artist': 'Sam Smith ft. Kim Petras',
                    'album': 'Unholy',
                    'popularity': 85,
                    'genre': 'Pop'
                }
            ],
            'artists': {
                'taylor swift': {
                    'name': 'Taylor Swift',
                    'genre': 'Pop/Country',
                    'albums': ['Midnights', 'Folklore', 'Evermore', '1989'],
                    'top_songs': ['Anti-Hero', 'Shake It Off', 'Love Story', 'Blank Space'],
                    'followers': '90M+',
                    'awards': 'Multiple Grammy Awards'
                },
                'harry styles': {
                    'name': 'Harry Styles',
                    'genre': 'Pop Rock',
                    'albums': ['Harry\'s House', 'Fine Line', 'Harry Styles'],
                    'top_songs': ['As It Was', 'Watermelon Sugar', 'Adore You'],
                    'followers': '50M+',
                    'awards': 'Grammy Award Winner'
                }
            }
        }
    
    def chat(self, user_input):
        """Main chat function"""
        user_input = user_input.lower().strip()
        
        # Add to conversation history
        self.conversation_history.append({
            'user': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process the input and generate response
        response = self._process_input(user_input)
        
        # Add response to history
        self.conversation_history[-1]['bot'] = response
        
        return response
    
    def _process_input(self, user_input):
        """Process user input and generate appropriate response"""
        
        # Trending songs requests
        if any(word in user_input for word in ['trending', 'popular', 'top', 'chart', 'hits']):
            return self._get_trending_songs()
        
        # Artist information requests
        elif any(word in user_input for word in ['artist', 'singer', 'about', 'tell me about']):
            artist_name = self._extract_artist_name(user_input)
            return self._get_artist_info(artist_name)
        
        # Lyrics requests
        elif 'lyrics' in user_input:
            song_info = self._extract_song_info(user_input)
            return self._get_lyrics(song_info)
        
        # Search requests
        elif any(word in user_input for word in ['search', 'find', 'look for']):
            query = self._extract_search_query(user_input)
            return self._search_songs(query)
        
        # General greetings
        elif any(word in user_input for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return self._get_greeting()
        
        # Help requests
        elif any(word in user_input for word in ['help', 'what can you do', 'commands']):
            return self._get_help()
        
        # Default response
        else:
            return self._get_default_response()
    
    def _get_trending_songs(self):
        """Return trending songs information"""
        response = "🎵 Here are the current trending songs:\n\n"
        
        for song in self.mock_data['trending_songs']:
            response += f"{song['rank']}. **{song['title']}** by {song['artist']}\n"
            response += f"   Album: {song['album']}\n"
            response += f"   Popularity: {song['popularity']}/100\n"
            response += f"   Genre: {song['genre']}\n\n"
        
        response += "Would you like more details about any of these songs or artists?"
        return response
    
    def _get_artist_info(self, artist_name):
        """Return artist information"""
        if not artist_name:
            return "Please tell me which artist you'd like to know about!"
        
        artist_key = artist_name.lower()
        
        if artist_key in self.mock_data['artists']:
            artist = self.mock_data['artists'][artist_key]
            response = f"🎤 **{artist['name']}**\n\n"
            response += f"🎵 Genre: {artist['genre']}\n"
            response += f"👥 Followers: {artist['followers']}\n"
            response += f"🏆 Awards: {artist['awards']}\n\n"
            response += f"📀 **Albums:** {', '.join(artist['albums'])}\n\n"
            response += f"🔥 **Top Songs:** {', '.join(artist['top_songs'])}\n\n"
            response += "Would you like to know more about any specific song or album?"
            return response
        else:
            return f"I don't have detailed information about {artist_name} in my current database. Try asking about Taylor Swift or Harry Styles!"
    
    def _get_lyrics(self, song_info):
        """Return song lyrics information"""
        if not song_info:
            return "Please tell me which song you'd like lyrics for!"
        
        return f"🎵 **{song_info}**\n\n📝 **Lyrics:**\n\n[This is a demo version - actual lyrics would appear here]\n\nIn a real implementation, this would fetch lyrics from Genius API or similar service."
    
    def _search_songs(self, query):
        """Search for songs"""
        if not query:
            return "Please tell me what song you're looking for!"
        
        # Simple search in mock data
        results = []
        for song in self.mock_data['trending_songs']:
            if (query.lower() in song['title'].lower() or 
                query.lower() in song['artist'].lower() or
                query.lower() in song['album'].lower()):
                results.append(song)
        
        if results:
            response = f"🔍 Found {len(results)} songs matching '{query}':\n\n"
            for song in results:
                response += f"• **{song['title']}** by {song['artist']}\n"
                response += f"  Album: {song['album']} | Popularity: {song['popularity']}/100\n\n"
            return response
        else:
            return f"No songs found matching '{query}'. Try searching for something else!"
    
    def _get_greeting(self):
        """Return a greeting message"""
        greetings = [
            "Hello! I'm your music chatbot. I can help you discover trending songs, learn about artists, and find lyrics!",
            "Hey there! Ready to explore some great music? Ask me about trending songs or your favorite artists!",
            "Hi! I'm here to help you with all things music. What would you like to know today?"
        ]
        return random.choice(greetings)
    
    def _get_help(self):
        """Return help information"""
        return """🎵 **Music Chatbot Help**

I can help you with:

🔥 **Trending Songs**: Ask "What are the trending songs?" or "Show me popular music"
🎤 **Artist Info**: Ask "Tell me about Taylor Swift" or "Info about Harry Styles"
📝 **Lyrics**: Ask "Get lyrics for [song name]" or "Lyrics of [song]"
🔍 **Search**: Ask "Search for [song/artist]" or "Find [music]"

Try asking me questions like:
• "What are the top songs right now?"
• "Tell me about Taylor Swift"
• "Search for Heat Waves"
• "Get lyrics for Anti-Hero"

What would you like to know about music?"""
    
    def _get_default_response(self):
        """Return a default response"""
        responses = [
            "I'm here to help you with music! Ask me about trending songs, artists, or search for music.",
            "I love talking about music! What would you like to know? Try asking about trending songs or your favorite artists.",
            "I can help you discover new music! Ask me about popular songs, artist information, or search for specific tracks.",
            "Music is amazing! I can help you with trending songs, artist details, lyrics, and music search. What interests you?"
        ]
        return random.choice(responses)
    
    def _extract_artist_name(self, text):
        """Extract artist name from text"""
        patterns = [
            r'about\s+([^?.!,]+)',
            r'artist\s+([^?.!,]+)',
            r'singer\s+([^?.!,]+)',
            r'tell me about\s+([^?.!,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_song_info(self, text):
        """Extract song information from text"""
        patterns = [
            r'lyrics\s+for\s+([^?.!,]+)',
            r'lyrics\s+of\s+([^?.!,]+)',
            r'get lyrics\s+([^?.!,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_search_query(self, text):
        """Extract search query from text"""
        patterns = [
            r'search\s+for\s+([^?.!,]+)',
            r'find\s+([^?.!,]+)',
            r'look for\s+([^?.!,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return ""


def main():
    """Main function to run the simple chatbot"""
    print("🎵 Simple Music Chatbot")
    print("=" * 50)
    print("Type 'quit' to exit, 'help' for commands")
    print("=" * 50)
    
    bot = SimpleMusicBot()
    
    while True:
        try:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🎵 Thanks for chatting about music! Goodbye!")
                break
            
            response = bot.chat(user_input)
            print(f"\nBot: {response}")
            
        except KeyboardInterrupt:
            print("\n\n🎵 Thanks for chatting about music! Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again!")


if __name__ == "__main__":
    main()
