import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "vision_platform")

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
DETECT_CLASSES = [
    item.strip().lower()
    for item in os.getenv("DETECT_CLASSES", "person,cell phone").split(",")
    if item.strip()
]

CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
LOG_COOLDOWN_SECONDS = float(os.getenv("LOG_COOLDOWN_SECONDS", "1.0"))
