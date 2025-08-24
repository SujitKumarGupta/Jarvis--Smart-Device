import os
import google.genai as genai
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY environment variable")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Write a short, 4-line poem about AI and nature."
)

print(response.text)
