import os
from google import genai
from dotenv import load_dotenv

load_dotenv(".secrets")

class LLMHelper:
    @staticmethod
    def get_gemini_model():
        api_key = os.getenv("GEMINI_API_KEY")
        # Initialize the client
        return genai.Client(api_key=api_key)