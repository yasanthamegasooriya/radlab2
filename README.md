# Music Chatbot - Trending Music Assistant

A sophisticated AI-powered chatbot designed to assist with trending music, artist information, and song lyrics. Built using Python, Flask, and various music APIs.

## 🎵 Features

- **Trending Songs**: Get the latest trending songs with detailed information
- **Artist Information**: Comprehensive artist details including discography, top tracks, and statistics
- **Lyrics Retrieval**: Fetch song lyrics from multiple sources
- **Music Search**: Search for songs by title, artist, or keywords
- **Interactive Chat**: Natural language conversation about music
- **Web Interface**: Beautiful, responsive web interface
- **API Endpoints**: RESTful API for integration with other applications

## 🚀 Technology Stack

- **Backend**: Python, Flask
- **AI/ML**: Transformers, LangChain, PyTorch
- **Music APIs**: Spotify Web API, Genius API
- **Frontend**: HTML, CSS, JavaScript, Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly

## 📁 Project Structure

```
radproject/
├── app.py                 # Flask web application
├── music_chatbot.py       # Main chatbot logic
├── music_service.py       # Music data services
├── streamlit_app.py       # Streamlit interface
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── templates/
│   └── index.html        # Web interface
└── README.md             # This file
```

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd radproject
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Edit the `.env` file and add your API keys:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   GENIUS_ACCESS_TOKEN=your_genius_access_token
   OPENAI_API_KEY=your_openai_api_key (optional)
   ```

## 🎯 API Keys Setup

### Spotify API
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new app
3. Copy the Client ID and Client Secret

### Genius API
1. Go to [Genius API](https://genius.com/api-clients)
2. Create a new API client
3. Copy the Access Token

## 🚀 Usage

### Running the Flask Web App
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

### Running the Streamlit App
```bash
streamlit run streamlit_app.py
```

### Command Line Interface
```bash
python music_chatbot.py
```

## 💬 Example Interactions

- **"What are the trending songs?"** - Get top 10 trending songs
- **"Tell me about Taylor Swift"** - Get artist information and top tracks
- **"Search for Shape of You"** - Search for specific songs
- **"Get lyrics for Blinding Lights"** - Fetch song lyrics
- **"Who sings Watermelon Sugar?"** - Get artist information for a song

## 🔧 API Endpoints

- `GET /` - Main web interface
- `POST /chat` - Chat with the bot
- `GET /trending` - Get trending songs
- `GET /artist/<name>` - Get artist information
- `GET /lyrics?song=<song>&artist=<artist>` - Get lyrics
- `GET /search?q=<query>` - Search songs

## 🎨 Features in Detail

### 1. Trending Music Analysis
- Real-time trending songs from Spotify
- Popularity metrics and rankings
- Duration and release date information
- Visual charts and analytics

### 2. Artist Intelligence
- Comprehensive artist profiles
- Discography and album information
- Top tracks and popularity metrics
- Social media and streaming statistics

### 3. Lyrics Integration
- Multiple lyrics sources
- Clean, formatted lyrics display
- Song metadata and credits
- Direct links to official sources

### 4. Natural Language Processing
- Intent recognition for music queries
- Context-aware responses
- Memory of conversation history
- Personalized recommendations

## 🤖 AI Model Information

The chatbot uses several AI models:
- **Microsoft DialoGPT**: For conversational responses
- **Transformers**: For natural language understanding
- **LangChain**: For conversation memory and chains
- **Custom NLP**: For music-specific intent recognition

## 📊 Why This is a "Rapid Project"

This project demonstrates rapid development capabilities because:

1. **Pre-trained Models**: Leverages existing LLMs instead of training from scratch
2. **API Integration**: Uses established music APIs for data
3. **Framework Efficiency**: Built on Flask and Streamlit for quick deployment
4. **Modular Design**: Separate services for easy scaling and maintenance
5. **Mock Data**: Includes fallback data for immediate testing
6. **Ready-to-Deploy**: Complete with web interface and API endpoints

## 🔮 Future Enhancements

- **Music Recommendations**: Personalized suggestions based on listening history
- **Voice Integration**: Voice input and output capabilities
- **Social Features**: Share music discoveries with friends
- **Advanced Analytics**: Deep insights into music trends
- **Multi-language Support**: Support for international music
- **Playlist Generation**: Create custom playlists based on preferences

## 🐛 Troubleshooting

### Common Issues:
1. **API Rate Limits**: The app includes mock data as fallback
2. **Model Loading**: Large models may take time to load initially
3. **Dependencies**: Ensure all packages are installed correctly
4. **API Keys**: Verify all API keys are set correctly in `.env`

### Performance Optimization:
- Use smaller models for faster response times
- Implement caching for frequently requested data
- Consider using cloud APIs for production deployment

## 📝 License

This project is for educational purposes. Please respect the terms of service of all APIs used.

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new music data sources
- Improving the AI conversation quality
- Enhancing the user interface
- Adding new features and capabilities

## 📞 Support

For questions or issues, please refer to the documentation or create an issue in the repository.

---

**Built with ❤️ for music lovers and AI enthusiasts**
