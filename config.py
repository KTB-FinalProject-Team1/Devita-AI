import os
from dotenv import load_dotenv


env = os.getenv('PYTHON_ENV', 'development')

if env == 'development':
    load_dotenv(".env.dev", override=True)
elif env == 'production':
    load_dotenv(".env.prod", override=True)

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
BACKEND_HOST = os.getenv('BACKEND_HOST')
BACKEND_PORT = os.getenv('BACKEND_PORT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
