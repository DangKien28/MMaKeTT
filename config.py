import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret")

  #GOOGLE
  GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
  GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

  #FACEBOOK
  FB_APP_ID = os.getenv("FB_APP_ID")
  FB_APP_SECRET = os.getenv("FB_APP_SECRET")