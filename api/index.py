import os
import sys
from dotenv import load_dotenv

backend_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "backend")
)

# Load the backend .env file when running locally
load_dotenv(os.path.join(backend_dir, ".env"))

sys.path.insert(0, backend_dir)

from main import app