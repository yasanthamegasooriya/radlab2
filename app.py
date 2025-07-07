from flask import Flask, render_template, request, jsonify
from simple_music_bot import SimpleMusicBot
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Initialize the simple chatbot (no heavy ML dependencies)
chatbot = SimpleMusicBot()

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
        
        response = chatbot.chat(user_input)
        
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
        # Use the mock data from simple bot
        trending_songs = chatbot.mock_data['trending_songs'][:limit]
        
        return jsonify({
            'songs': trending_songs,
            'status': 'success'
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
        artist_key = artist_name.lower()
        
        if artist_key in chatbot.mock_data['artists']:
            artist_info = chatbot.mock_data['artists'][artist_key]
            return jsonify({
                'artist': artist_info,
                'status': 'success'
            })
        else:
            return jsonify({
                'error': f'Artist {artist_name} not found in database',
                'status': 'error'
            }), 404
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/lyrics')
def lyrics():
    """Get song lyrics"""
    try:
        song = request.args.get('song', '')
        artist = request.args.get('artist', '')
        
        if not song:
            return jsonify({'error': 'Song parameter is required'}), 400
        
        # Simple lyrics response using the simple bot's method
        lyrics_data = {
            'title': song,
            'artist': artist or 'Unknown',
            'lyrics': f"[Lyrics for '{song}' by {artist or 'Unknown'} would appear here]\n\n[This is a demo version - please configure your Genius API key to get actual lyrics]",
            'url': 'https://genius.com/demo-url'
        }
        
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
        
        # Simple search in mock data
        results = []
        for song in chatbot.mock_data['trending_songs']:
            if (query.lower() in song['title'].lower() or 
                query.lower() in song['artist'].lower()):
                results.append(song)
        
        return jsonify({
            'songs': results[:limit],
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
        'message': 'Music Chatbot is running!',
        'features': [
            'Trending Songs',
            'Artist Information', 
            'Music Search',
            'Chat Interface',
            'Lyrics (Demo)'
        ]
    })

if __name__ == '__main__':
    print("🎵 Starting Music Chatbot Web Server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🔗 API endpoints available:")
    print("   - GET  /health     - Health check")
    print("   - POST /chat       - Chat with bot")
    print("   - GET  /trending   - Get trending songs")
    print("   - GET  /search     - Search songs")
    print("   - GET  /lyrics     - Get lyrics (demo)")
    print("   - GET  /artist/<name> - Get artist info")
    print("💡 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
