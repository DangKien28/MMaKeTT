import os
BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
SECRET_KEY = 'dev-secret-key'
PERSIST_FILE = os.path.join(BASE_DIR, 'sellers.json')
