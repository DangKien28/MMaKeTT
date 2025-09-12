import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret")
  GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
  GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")