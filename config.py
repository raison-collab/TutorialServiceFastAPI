import os

from dotenv import load_dotenv

load_dotenv()

#  Database config
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Auth token key config
TOKEN_SECRET = os.getenv("TOKEN_SECRET_KEY")

# Server settings
SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PROTOCOL = os.getenv("SERVER_PROTOCOL")

# Debug status
DEBUG = bool(os.getenv("DEBUG"))
