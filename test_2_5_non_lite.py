import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    # Trying the non-lite version which appeared unused in screenshots
    model = genai.GenerativeModel('gemini-2.5-flash') 
    response = model.generate_content("Hello")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Failed: {e}")
