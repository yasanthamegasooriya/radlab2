#!/bin/bash

# Music Chatbot Launcher
# This script helps you run different versions of the chatbot

echo "🎵 Music Chatbot Launcher"
echo "========================="
echo ""
echo "Choose how you want to run the chatbot:"
echo "1. Simple Console Chat (no API keys needed)"
echo "2. Flask Web App (opens in browser)"
echo "3. Streamlit Dashboard (interactive)"
echo "4. Exit"
echo ""

while true; do
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            echo "🎵 Starting Simple Console Chat..."
            /Users/yasanthamegasooriya/Documents/mscUom/radproject/.venv/bin/python simple_music_bot.py
            ;;
        2)
            echo "🌐 Starting Flask Web App..."
            echo "The app will be available at: http://localhost:5000"
            /Users/yasanthamegasooriya/Documents/mscUom/radproject/.venv/bin/python app.py
            ;;
        3)
            echo "📊 Starting Streamlit Dashboard..."
            echo "The dashboard will open in your browser automatically"
            /Users/yasanthamegasooriya/Documents/mscUom/radproject/.venv/bin/python -m streamlit run streamlit_app.py
            ;;
        4)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter 1, 2, 3, or 4."
            ;;
    esac
    
    echo ""
    echo "Press any key to continue..."
    read -n 1 -s
    echo ""
done
