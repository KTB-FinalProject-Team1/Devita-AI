import os
from dotenv import load_dotenv

# Load environment
env = os.getenv('PYTHON_ENV')
if not env:
    raise ValueError("Missing required environment variable: PYTHON_ENV")

if env == 'development':
    load_dotenv(".env.dev")
elif env == 'production':
    load_dotenv(".env.prod")
else:
    raise ValueError(f"Invalid PYTHON_ENV value: {env}")

# Load required environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = int(os.getenv('DATABASE_PORT', 8000))  # Default port: 8000
BACKEND_HOST = os.getenv('BACKEND_HOST')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8080))  # Default port: 8080
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate critical variables
if not DATABASE_HOST:
    raise ValueError("Missing required environment variable: DATABASE_HOST")
if not OPENAI_API_KEY:
    raise ValueError("Missing required environment variable: OPENAI_API_KEY")
