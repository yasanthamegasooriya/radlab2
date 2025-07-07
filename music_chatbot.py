import os
from typing import Dict, List, Any
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from langchain.llms.base import LLM
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from music_service import MusicDataService, LyricsService
import json
import re

class MusicChatbot:
    """Main chatbot class that handles music-related conversations"""
    
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.music_service = MusicDataService()
        self.lyrics_service = LyricsService()
        self.model_name = model_name
        self.conversation_memory = ConversationBufferMemory()
        self.setup_llm()
        self.setup_conversation_chain()
    
    def setup_llm(self):
        """Setup the language model for conversation"""
        try:
            # Try to use a local model first
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.text_generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=1000,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
        except Exception as e:
            print(f"Error setting up model: {e}")
            self.text_generator = None
    
    def setup_conversation_chain(self):
        """Setup the conversation chain with memory"""
        template = """
        You are a music assistant chatbot specialized in trending music, artists, and lyrics.
        
        Your capabilities include:
        - Providing information about trending songs
        - Sharing artist details and discography
        - Fetching song lyrics
        - Answering music-related questions
        - Making music recommendations
        
        Always be helpful, enthusiastic about music, and provide accurate information.
        
        Current conversation:
        {history}
        
        User: {input}
        Assistant:"""
        
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate appropriate response"""
        user_input_lower = user_input.lower()
        
        # Check for specific music-related intents
        if self._is_trending_songs_request(user_input_lower):
            return self._handle_trending_songs_request(user_input)
        elif self._is_artist_info_request(user_input_lower):
            return self._handle_artist_info_request(user_input)
        elif self._is_lyrics_request(user_input_lower):
            return self._handle_lyrics_request(user_input)
        elif self._is_song_search_request(user_input_lower):
            return self._handle_song_search_request(user_input)
        else:
            return self._handle_general_conversation(user_input)
    
    def _is_trending_songs_request(self, text: str) -> bool:
        """Check if user is asking for trending songs"""
        trending_keywords = [
            'trending', 'popular', 'top songs', 'chart', 'hits',
            'what\'s hot', 'current hits', 'latest songs'
        ]
        return any(keyword in text for keyword in trending_keywords)
    
    def _is_artist_info_request(self, text: str) -> bool:
        """Check if user is asking for artist information"""
        artist_keywords = [
            'artist', 'singer', 'band', 'musician', 'about',
            'biography', 'discography', 'albums'
        ]
        return any(keyword in text for keyword in artist_keywords)
    
    def _is_lyrics_request(self, text: str) -> bool:
        """Check if user is asking for lyrics"""
        lyrics_keywords = ['lyrics', 'words', 'text of song', 'song words']
        return any(keyword in text for keyword in lyrics_keywords)
    
    def _is_song_search_request(self, text: str) -> bool:
        """Check if user is searching for a specific song"""
        search_keywords = ['search', 'find', 'look for', 'song called']
        return any(keyword in text for keyword in search_keywords)
    
    def _handle_trending_songs_request(self, user_input: str) -> str:
        """Handle requests for trending songs"""
        try:
            # Extract number if mentioned
            number_match = re.search(r'\d+', user_input)
            limit = int(number_match.group()) if number_match else 10
            limit = min(limit, 20)  # Cap at 20 songs
            
            trending_songs = self.music_service.get_trending_songs(limit=limit)
            
            if trending_songs:
                response = f"🎵 Here are the top {len(trending_songs)} trending songs right now:\n\n"
                
                for song in trending_songs:
                    duration_minutes = song['duration_ms'] // 60000
                    duration_seconds = (song['duration_ms'] % 60000) // 1000
                    
                    response += f"{song['rank']}. **{song['title']}** by {song['artist']}\n"
                    response += f"   Album: {song['album']}\n"
                    response += f"   Duration: {duration_minutes}:{duration_seconds:02d}\n"
                    response += f"   Popularity: {song['popularity']}/100\n\n"
                
                response += "Would you like more details about any of these songs, or their lyrics?"
                return response
            else:
                return "I'm sorry, I couldn't fetch the trending songs right now. Please try again later."
                
        except Exception as e:
            return f"I encountered an error while fetching trending songs: {str(e)}"
    
    def _handle_artist_info_request(self, user_input: str) -> str:
        """Handle requests for artist information"""
        try:
            # Extract artist name from the input
            artist_name = self._extract_artist_name(user_input)
            
            if not artist_name:
                return "Please specify which artist you'd like to know about!"
            
            artist_info = self.music_service.get_artist_info(artist_name)
            
            if artist_info:
                response = f"🎤 **{artist_info['name']}**\n\n"
                response += f"👥 Followers: {artist_info['followers']:,}\n"
                response += f"📈 Popularity: {artist_info['popularity']}/100\n"
                response += f"🎵 Genres: {', '.join(artist_info['genres'])}\n\n"
                
                if artist_info['top_tracks']:
                    response += "🔥 **Top Tracks:**\n"
                    for track in artist_info['top_tracks'][:5]:
                        response += f"   • {track['name']} (Popularity: {track['popularity']}/100)\n"
                    response += "\n"
                
                if artist_info['albums']:
                    response += "💿 **Recent Albums:**\n"
                    for album in artist_info['albums'][:3]:
                        response += f"   • {album['name']} ({album['release_date']})\n"
                
                response += f"\n🎧 [Listen on Spotify]({artist_info['spotify_url']})"
                return response
            else:
                return f"I couldn't find information about the artist '{artist_name}'. Please check the spelling or try a different name."
                
        except Exception as e:
            return f"I encountered an error while fetching artist information: {str(e)}"
    
    def _handle_lyrics_request(self, user_input: str) -> str:
        """Handle requests for song lyrics"""
        try:
            # Extract song and artist from input
            song_info = self._extract_song_and_artist(user_input)
            
            if not song_info['song']:
                return "Please specify which song you'd like the lyrics for!"
            
            lyrics_data = self.lyrics_service.get_lyrics(
                song_info['song'], 
                song_info['artist'] or 'Unknown'
            )
            
            if lyrics_data:
                response = f"🎵 **{lyrics_data['title']}** by {lyrics_data['artist']}\n\n"
                response += "📝 **Lyrics:**\n"
                response += f"{lyrics_data['lyrics'][:500]}..."  # Truncate for demo
                response += f"\n\n🔗 [Full lyrics on Genius]({lyrics_data['url']})"
                return response
            else:
                return f"I couldn't find lyrics for '{song_info['song']}'. Please try a different song."
                
        except Exception as e:
            return f"I encountered an error while fetching lyrics: {str(e)}"
    
    def _handle_song_search_request(self, user_input: str) -> str:
        """Handle song search requests"""
        try:
            # Extract search query
            search_query = self._extract_search_query(user_input)
            
            if not search_query:
                return "Please specify what song you're looking for!"
            
            songs = self.music_service.search_song(search_query, limit=5)
            
            if songs:
                response = f"🔍 Found {len(songs)} songs matching '{search_query}':\n\n"
                
                for i, song in enumerate(songs, 1):
                    duration_minutes = song['duration_ms'] // 60000
                    duration_seconds = (song['duration_ms'] % 60000) // 1000
                    
                    response += f"{i}. **{song['title']}** by {song['artist']}\n"
                    response += f"   Album: {song['album']}\n"
                    response += f"   Duration: {duration_minutes}:{duration_seconds:02d}\n"
                    response += f"   Popularity: {song['popularity']}/100\n\n"
                
                response += "Would you like more details about any of these songs?"
                return response
            else:
                return f"I couldn't find any songs matching '{search_query}'. Please try a different search term."
                
        except Exception as e:
            return f"I encountered an error while searching for songs: {str(e)}"
    
    def _handle_general_conversation(self, user_input: str) -> str:
        """Handle general conversation about music"""
        try:
            if self.text_generator:
                # Use the LLM for general conversation
                prompt = f"Music Assistant: {user_input}\n\nResponse:"
                
                result = self.text_generator(
                    prompt,
                    max_length=len(prompt.split()) + 100,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                response = result[0]['generated_text'][len(prompt):].strip()
                
                # Add music context if response is too generic
                if len(response) < 20:
                    response = self._generate_music_context_response(user_input)
                
                return response
            else:
                return self._generate_music_context_response(user_input)
                
        except Exception as e:
            return self._generate_music_context_response(user_input)
    
    def _generate_music_context_response(self, user_input: str) -> str:
        """Generate a contextual response about music"""
        responses = [
            "I'm here to help you with all things music! You can ask me about trending songs, artist information, lyrics, or search for specific tracks.",
            "Music is such a wonderful art form! What would you like to know about today's music scene?",
            "I love talking about music! Whether you're interested in pop, rock, hip-hop, or any other genre, I'm here to help.",
            "Let's explore the world of music together! Ask me about your favorite artists or discover new trending songs.",
            "I'm your personal music assistant! I can help you find trending songs, get artist details, fetch lyrics, and much more."
        ]
        
        import random
        return random.choice(responses)
    
    def _extract_artist_name(self, text: str) -> str:
        """Extract artist name from user input"""
        # Simple regex patterns to extract artist names
        patterns = [
            r'about\s+([^?.!]+)',
            r'artist\s+([^?.!]+)',
            r'singer\s+([^?.!]+)',
            r'band\s+([^?.!]+)',
            r'musician\s+([^?.!]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_song_and_artist(self, text: str) -> Dict[str, str]:
        """Extract song title and artist from user input"""
        # Simple patterns to extract song and artist
        patterns = [
            r'lyrics\s+for\s+([^?.!]+)\s+by\s+([^?.!]+)',
            r'lyrics\s+of\s+([^?.!]+)\s+by\s+([^?.!]+)',
            r'([^?.!]+)\s+by\s+([^?.!]+)\s+lyrics',
            r'lyrics\s+([^?.!]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return {
                        'song': match.group(1).strip(),
                        'artist': match.group(2).strip()
                    }
                else:
                    return {
                        'song': match.group(1).strip(),
                        'artist': None
                    }
        
        return {'song': '', 'artist': None}
    
    def _extract_search_query(self, text: str) -> str:
        """Extract search query from user input"""
        patterns = [
            r'search\s+for\s+([^?.!]+)',
            r'find\s+([^?.!]+)',
            r'look\s+for\s+([^?.!]+)',
            r'song\s+called\s+([^?.!]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def chat(self, user_input: str) -> str:
        """Main chat interface"""
        try:
            response = self.process_user_input(user_input)
            
            # Store conversation in memory
            self.conversation_memory.chat_memory.add_user_message(user_input)
            self.conversation_memory.chat_memory.add_ai_message(response)
            
            return response
            
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}. Please try again!"


if __name__ == "__main__":
    # Simple command-line interface for testing
    print("🎵 Music Chatbot initialized! Type 'quit' to exit.")
    print("Try asking: 'What are the trending songs?' or 'Tell me about Taylor Swift'")
    
    chatbot = MusicChatbot()
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! 🎵")
            break
        
        response = chatbot.chat(user_input)
        print(f"\nBot: {response}")
