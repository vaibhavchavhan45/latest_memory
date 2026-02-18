from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
CHAT_DATABASE_URL = os.getenv("CHAT_DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")