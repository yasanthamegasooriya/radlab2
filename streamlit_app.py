import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from music_chatbot import MusicChatbot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page config
st.set_page_config(
    page_title="Music Chatbot",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        border-left-color: #667eea;
    }
    
    .song-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MusicChatbot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown("""
    <div class="main-header">
        <h1>🎵 Music Chatbot</h1>
        <p>Your Personal AI Assistant for Trending Music, Artists, and Lyrics</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎵 Music Dashboard")

# Quick Actions
st.sidebar.subheader("🚀 Quick Actions")
if st.sidebar.button("📈 Show Trending Songs"):
    st.session_state.quick_action = "What are the trending songs?"
if st.sidebar.button("🎤 Artist Info (Taylor Swift)"):
    st.session_state.quick_action = "Tell me about Taylor Swift"
if st.sidebar.button("🔍 Search Songs"):
    st.session_state.quick_action = "Search for Shape of You"
if st.sidebar.button("📝 Get Lyrics"):
    st.session_state.quick_action = "Get lyrics for Blinding Lights"

# Trending Songs in Sidebar
st.sidebar.subheader("🔥 Current Top Songs")
try:
    trending_songs = st.session_state.chatbot.music_service.get_trending_songs(limit=5)
    for song in trending_songs:
        st.sidebar.markdown(f"""
            <div class="song-card">
                <strong>{song['rank']}. {song['title']}</strong><br>
                <small>by {song['artist']}</small><br>
                <small>Popularity: {song['popularity']}/100</small>
            </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"Error loading trending songs: {str(e)}")

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat with Music Bot")
    
    # Chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['type'] == 'user':
                st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong> {message['content']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>Bot:</strong> {message['content']}
                    </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me about music...")
    
    # Handle quick actions
    if 'quick_action' in st.session_state:
        user_input = st.session_state.quick_action
        del st.session_state.quick_action
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'type': 'user',
            'content': user_input
        })
        
        # Get bot response
        with st.spinner("Thinking about music... 🎵"):
            try:
                response = st.session_state.chatbot.chat(user_input)
                st.session_state.chat_history.append({
                    'type': 'bot',
                    'content': response
                })
            except Exception as e:
                st.session_state.chat_history.append({
                    'type': 'bot',
                    'content': f"Sorry, I encountered an error: {str(e)}"
                })
        
        st.rerun()

with col2:
    st.subheader("📊 Music Analytics")
    
    # Show trending songs chart
    try:
        trending_songs = st.session_state.chatbot.music_service.get_trending_songs(limit=10)
        
        if trending_songs:
            df = pd.DataFrame(trending_songs)
            
            # Popularity chart
            fig = px.bar(
                df, 
                x='title', 
                y='popularity',
                title='Song Popularity Chart',
                labels={'popularity': 'Popularity Score', 'title': 'Song Title'}
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Duration chart
            df['duration_minutes'] = df['duration_ms'] / 60000
            fig2 = px.scatter(
                df, 
                x='duration_minutes', 
                y='popularity',
                size='rank',
                hover_data=['title', 'artist'],
                title='Duration vs Popularity'
            )
            st.plotly_chart(fig2, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎵 Music Chatbot - Built with Streamlit, Python, and Music APIs</p>
        <p>Ask me about trending songs, artists, lyrics, or search for your favorite music!</p>
    </div>
""", unsafe_allow_html=True)

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()
