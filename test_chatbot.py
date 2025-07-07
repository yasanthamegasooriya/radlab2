#!/usr/bin/env python3
"""
Music Chatbot Test Script
This script tests all components of the music chatbot
"""

def test_simple_bot():
    """Test the simple music bot"""
    print("🎵 Testing Simple Music Bot...")
    try:
        from simple_music_bot import SimpleMusicBot
        bot = SimpleMusicBot()
        
        # Test trending songs
        response = bot.chat("What are the trending songs?")
        assert "Anti-Hero" in response
        print("✅ Trending songs test passed")
        
        # Test artist info
        response = bot.chat("Tell me about Taylor Swift")
        assert "Taylor Swift" in response
        print("✅ Artist info test passed")
        
        # Test search
        response = bot.chat("Search for Heat Waves")
        assert "Heat Waves" in response
        print("✅ Search test passed")
        
        print("✅ Simple bot: ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Simple bot test failed: {e}")
        return False

def test_flask_imports():
    """Test Flask app imports"""
    print("\n🌐 Testing Flask App Imports...")
    try:
        from flask import Flask
        print("✅ Flask imported")
        
        from simple_music_bot import SimpleMusicBot
        print("✅ SimpleMusicBot imported")
        
        # Test creating app components
        app = Flask(__name__)
        bot = SimpleMusicBot()
        print("✅ App components created")
        
        print("✅ Flask imports: ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Flask import test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎵 Music Chatbot - Component Test Suite")
    print("=" * 50)
    
    results = []
    
    # Test simple bot
    results.append(test_simple_bot())
    
    # Test Flask imports
    results.append(test_flask_imports())
    
    # Summary
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 ALL TESTS PASSED! Your Music Chatbot is ready!")
        print("\n🚀 How to run:")
        print("   Console: python simple_music_bot.py")
        print("   Web App: python app.py")
        print("   Browser: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    print("\n📁 Your project structure:")
    import os
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    for file in sorted(files):
        print(f"   {file}")

if __name__ == "__main__":
    main()
