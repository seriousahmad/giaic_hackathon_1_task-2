#!/usr/bin/env python3
"""
Test script to verify if the Gemini API key is valid and working.
"""
import asyncio
import os
from app.services.gemini_client import gemini_client


async def test_api_key():
    """
    Test the Gemini API key by making a simple health check call.
    """
    print("Testing Gemini API key...")

    # Check if the API key is set in environment
    if not os.getenv('GEMINI_API_KEY'):
        print("ERROR: GEMINI_API_KEY environment variable is not set!")
        print("Please add your actual API key to the backend/.env file")
        print("Your API key should start with 'AIza' and be about 39 characters long")
        return False

    # Perform health check
    try:
        print("Performing health check...")
        is_healthy = await gemini_client.health_check()

        if is_healthy:
            print("SUCCESS: Gemini API key is valid and working!")

            # Try a simple test call
            print("Testing with a simple query...")
            result = await gemini_client.generate_answer(
                question="Hello, are you working properly?",
                max_tokens=20
            )
            print(f"Response: {result['answer']}")
            print(f"Token usage: {result['usage']}")
            return True
        else:
            print("ERROR: Gemini API key is invalid or not working properly")
            return False

    except Exception as e:
        print(f"ERROR: Error testing API key: {str(e)}")
        return False


if __name__ == "__main__":
    # Load environment variables from .env file
    from app.config.settings import settings

    print("Gemini API Key Test")
    print("=" * 30)

    # Check if the key in settings is the example key
    if settings.gemini_api_key == "AIzaSyD_Pbe4ygFmBxyJfC0fhsBCxwgaaJOCdlE":
        print("WARNING: You are using the example API key!")
        print("\nTo test with your actual API key:")
        print("1. Get your API key from: https://aistudio.google.com/app/apikey")
        print("2. Open the backend/.env file")
        print("3. Replace the example key with your actual key:")
        print("   GEMINI_API_KEY=your_actual_api_key_here")
        print("4. Save the file and run this script again")
        exit(1)

    success = asyncio.run(test_api_key())

    if success:
        print("\nSUCCESS: Your Gemini API key is working correctly!")
    else:
        print("\nERROR: There was an issue with your Gemini API key.")
        print("Make sure:")
        print("  1. Your API key is correctly set in backend/.env")
        print("  2. Your API key is valid (starts with 'AIza')")
        print("  3. Your Google AI Studio account is properly configured")
        print("  4. Your API key has the necessary permissions enabled")
        print("  5. Your API key hasn't exceeded usage limits")