from flask import Flask, render_template, request, jsonify
from real_music_service import RealMusicService
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Initialize the real music service with Spotify and OpenAI APIs
music_service = RealMusicService()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        user_input = request.json.get('message', '')
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process different types of queries
        user_lower = user_input.lower()
        
        if 'trending' in user_lower or 'popular' in user_lower:
            trending = music_service.get_trending_songs(limit=5)
            if trending:
                song_list = "\n".join([f"{song['rank']}. {song['title']} by {song['artist']}" for song in trending[:5]])
                response = f"🎵 Here are the current trending songs:\n\n{song_list}"
            else:
                response = "Sorry, I couldn't fetch trending songs right now. Please try again later."
        
        elif 'lyrics' in user_lower:
            # Extract song and artist from query if possible
            words = user_input.split()
            if len(words) > 2:
                # Simple extraction - look for patterns like "lyrics for Song by Artist"
                try:
                    if 'by' in user_lower:
                        parts = user_input.split(' by ')
                        song_part = parts[0].replace('lyrics for', '').replace('lyrics', '').strip()
                        artist_part = parts[1].strip()
                    else:
                        song_part = ' '.join(words[1:3])  # Take next 2 words as song title
                        artist_part = "Unknown Artist"
                    
                    lyrics_data = music_service.generate_ai_lyrics(song_part, artist_part)
                    response = f"🎤 AI-Generated Lyrics for '{lyrics_data['title']}':\n\n{lyrics_data['lyrics'][:500]}...\n\n💡 {lyrics_data['note']}"
                except:
                    response = "Please specify a song title for AI-generated lyrics. Example: 'Generate lyrics for My Song by Artist Name'"
            else:
                response = "Please specify a song title for AI-generated lyrics. Example: 'Generate lyrics for My Song by Artist Name'"
        
        elif any(word in user_lower for word in ['search', 'find', 'look for']):
            # Extract search query
            search_terms = user_input.lower()
            for remove_word in ['search for', 'find', 'look for', 'search']:
                search_terms = search_terms.replace(remove_word, '').strip()
            
            if search_terms:
                results = music_service.search_song(search_terms, limit=3)
                if results:
                    song_list = "\n".join([f"• {song['title']} by {song['artist']} ({song['album']})" for song in results])
                    response = f"🔍 Found these songs for '{search_terms}':\n\n{song_list}"
                else:
                    response = f"No songs found for '{search_terms}'. Try a different search term."
            else:
                response = "Please specify what you'd like to search for."
        
        elif 'artist' in user_lower or 'about' in user_lower:
            # Extract artist name
            words = user_input.split()
            artist_name = None
            for i, word in enumerate(words):
                if word.lower() in ['artist', 'about']:
                    if i + 1 < len(words):
                        artist_name = ' '.join(words[i+1:])
                        break
            
            if artist_name:
                artist_info = music_service.get_artist_info(artist_name)
                if artist_info:
                    response = f"🎤 {artist_info['name']}\n\nFollowers: {artist_info.get('followers', 'N/A'):,}\nGenres: {', '.join(artist_info.get('genres', ['Unknown']))}\nPopularity: {artist_info.get('popularity', 'N/A')}/100"
                else:
                    response = f"Sorry, I couldn't find information about artist '{artist_name}'"
            else:
                response = "Please specify an artist name. Example: 'Tell me about Taylor Swift'"
        
        else:
            response = """🎵 Welcome to the AI Music Chatbot! I can help you with:

• "What's trending?" - Get current popular songs
• "Search for [song name]" - Find specific songs  
• "Generate lyrics for [song] by [artist]" - AI-generated original lyrics
• "Tell me about [artist]" - Get artist information

What would you like to explore today?"""
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/trending')
def trending():
    """Get trending songs"""
    try:
        limit = request.args.get('limit', 10, type=int)
        country = request.args.get('country', 'US')
        
        trending_songs = music_service.get_trending_songs(limit=limit, country=country)
        
        return jsonify({
            'songs': trending_songs,
            'status': 'success',
            'count': len(trending_songs)
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/artist/<artist_name>')
def artist_info(artist_name):
    """Get artist information"""
    try:
        artist_data = music_service.get_artist_info(artist_name)
        
        if artist_data and artist_data.get('name'):
            return jsonify({
                'artist': artist_data,
                'status': 'success'
            })
        else:
            return jsonify({
                'error': f'Artist {artist_name} not found',
                'status': 'error'
            }), 404
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/lyrics')
def lyrics():
    """Get AI-generated song lyrics"""
    try:
        song = request.args.get('song', '')
        artist = request.args.get('artist', '')
        style = request.args.get('style', 'pop')
        
        if not song:
            return jsonify({'error': 'Song parameter is required'}), 400
        
        if not artist:
            artist = 'Unknown Artist'
        
        # Generate AI lyrics using OpenAI
        lyrics_data = music_service.generate_ai_lyrics(song, artist, style)
        
        return jsonify({
            'lyrics': lyrics_data,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/search')
def search():
    """Search for songs"""
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 5, type=int)
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        # Search using Spotify API
        results = music_service.search_song(query, limit=limit)
        
        return jsonify({
            'songs': results,
            'status': 'success',
            'query': query,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/analysis')
def analysis():
    """Get AI-powered song analysis"""
    try:
        song = request.args.get('song', '')
        artist = request.args.get('artist', '')
        
        if not song:
            return jsonify({'error': 'Song parameter is required'}), 400
        
        if not artist:
            artist = 'Unknown Artist'
        
        # Get AI analysis using OpenAI
        analysis_text = music_service.get_song_analysis(song, artist)
        
        return jsonify({
            'analysis': {
                'song': song,
                'artist': artist,
                'text': analysis_text
            },
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Music Chatbot is running!',
        'features': [
            'Real-time Trending Songs (Spotify)',
            'Artist Information (Spotify)', 
            'Music Search (Spotify)',
            'AI-Generated Lyrics (OpenAI)',
            'AI Song Analysis (OpenAI)',
            'Interactive Chat Interface'
        ],
        'apis': {
            'spotify': music_service.spotify is not None,
            'openai': music_service.openai_client is not None
        }
    })

if __name__ == '__main__':
    print("🎵 Starting AI Music Chatbot Web Server...")
    print("📱 Open your browser to: http://localhost:3000")
    print("🔗 API endpoints available:")
    print("   - GET  /health      - Health check with API status")
    print("   - POST /chat        - AI-powered chat interface")
    print("   - GET  /trending    - Real trending songs from Spotify")
    print("   - GET  /search      - Search songs via Spotify API")
    print("   - GET  /lyrics      - AI-generated lyrics via OpenAI")
    print("   - GET  /analysis    - AI song analysis via OpenAI")
    print("   - GET  /artist/<n>  - Real artist info from Spotify")
    print("🤖 AI Features:")
    print("   - Spotify: Real-time music data")
    print("   - OpenAI: AI-generated lyrics & analysis")
    print("💡 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=3000)
