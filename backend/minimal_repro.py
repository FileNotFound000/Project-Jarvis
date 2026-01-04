import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("No API key found")
    exit(1)

genai.configure(api_key=api_key)

try:
    print("Testing GenerativeModel with empty system_instruction...")
    model = genai.GenerativeModel("gemini-2.5-flash-lite", system_instruction="")
    print("Success!")
except Exception as e:
    print(f"Error with empty string: {e}")

try:
    print("Testing GenerativeModel with None system_instruction...")
    model = genai.GenerativeModel("gemini-2.5-flash-lite", system_instruction=None)
    print("Success!")
except Exception as e:
    print(f"Error with None: {e}")
