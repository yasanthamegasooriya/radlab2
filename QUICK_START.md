# 🎵 Music Chatbot - Quick Start Guide

## ✅ Environment Setup Complete!

Your virtual environment is ready and all packages are installed. Here's how to run your Music Chatbot:

## 🚀 Running Options

### Option 1: Simple Console Chat (Recommended for Testing)
```bash
# Run the simple console chatbot
/Users/yasanthamegasooriya/Documents/mscUom/radproject/.venv/bin/python simple_music_bot.py
```

### Option 2: Web Application (Simplified)
```bash
# Run the simple Flask web app (no heavy ML dependencies)
/Users/yasanthamegasooriya/Documents/mscUom/radproject/.venv/bin/python app_simple.py

# Then open your browser to: http://localhost:5000
```

### Option 3: Original Web App (Advanced - requires more packages)
```bash
# Run the full Flask web app (requires all ML packages)
/Users/yasanthamegasooriya/Documents/mscUom/radproject/.venv/bin/python app.py

# Then open your browser to: http://localhost:5000
```

### Option 4: Easy Launcher (All-in-One)
```bash
# Run the launcher script
./run_chatbot.sh

# Then choose your preferred option from the menu
```

## 🎯 What Each Option Does

### 1. Simple Console Chat
- **Best for**: Quick testing and demonstrations
- **Features**: All core chatbot functionality
- **Requirements**: No API keys needed
- **What it does**: Command-line interface with mock music data

### 2. Flask Web App
- **Best for**: Professional presentation
- **Features**: Beautiful web interface, REST API
- **Requirements**: Optional API keys for live data
- **What it does**: Full web application with chat interface

### 3. Streamlit Dashboard
- **Best for**: Data visualization and analytics
- **Features**: Interactive charts, real-time updates
- **Requirements**: Optional API keys for live data
- **What it does**: Analytics dashboard with music trends

## 🎵 Example Interactions

Try these sample queries:
- "What are the trending songs?"
- "Tell me about Taylor Swift"
- "Search for Heat Waves"
- "Get lyrics for Anti-Hero"
- "Help me find new music"

## 🔧 Adding Real API Keys (Optional)

To get live music data instead of mock data:

1. **Edit the `.env` file**:
   ```
   SPOTIFY_CLIENT_ID=your_actual_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_actual_spotify_client_secret
   GENIUS_ACCESS_TOKEN=your_actual_genius_token
   ```

2. **Get API Keys**:
   - Spotify: https://developer.spotify.com/dashboard/
   - Genius: https://genius.com/api-clients

## 📱 Features Available

✅ **Trending Songs**: Get current top songs
✅ **Artist Information**: Detailed artist profiles
✅ **Music Search**: Find songs by title or artist
✅ **Lyrics**: Get song lyrics (with Genius API)
✅ **Conversation**: Natural language chat about music
✅ **Analytics**: Visual charts and trends
✅ **Responsive Design**: Works on mobile and desktop

## 🆘 Troubleshooting

If you encounter issues:

1. **Virtual Environment**: Make sure it's activated:
   ```bash
   source venv/bin/activate
   ```

2. **Dependencies**: If packages are missing:
   ```bash
   pip install -r requirements.txt
   ```

3. **Port Issues**: If port 5000 is busy:
   ```bash
   python app.py --port 5001
   ```

## 🎉 Success!

Your Music Chatbot is ready to use! Start with the simple console version to test all features, then move to the web interface for the full experience.

**Current Status**: ✅ Environment Ready | ✅ Packages Installed | ✅ Bot Tested
