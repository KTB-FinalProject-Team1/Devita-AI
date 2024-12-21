import os
from dotenv import load_dotenv

# Always load the base .env file
load_dotenv()

# Determine the environment and load the specific .env file
env = os.getenv('PYTHON_ENV', 'production')  # 기본값을 'production'으로 설정

if env == 'development':
    load_dotenv(".env.dev", override=True)  # Override base variables with development-specific ones
elif env == 'production':
    load_dotenv(".env.prod", override=True)  # Override base variables with production-specific ones
else:
    raise ValueError(f"Invalid PYTHON_ENV value: {env}")

# Load required environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = int(os.getenv('DATABASE_PORT', 8000))  # Default port: 8000
BACKEND_HOST = os.getenv('BACKEND_HOST')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8080))  # Default port: 8080
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate critical variables
missing_vars = []
if not DATABASE_HOST:
    missing_vars.append("DATABASE_HOST")
if not OPENAI_API_KEY:
    missing_vars.append("OPENAI_API_KEY")

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
