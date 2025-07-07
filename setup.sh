#!/bin/bash

# Music Chatbot Setup Script
# This script sets up the environment and installs dependencies

echo "🎵 Setting up Music Chatbot environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data
mkdir -p models

echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Set up your API keys in the .env file"
echo "3. Run the Flask app: python app.py"
echo "4. Or run the Streamlit app: streamlit run streamlit_app.py"
echo ""
echo "🔑 Don't forget to add your API keys to the .env file!"
echo "   - Spotify Client ID and Secret"
echo "   - Genius Access Token"
echo "   - OpenAI API Key (optional)"
