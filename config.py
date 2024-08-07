import os

from dotenv import load_dotenv

load_dotenv()

#  Database config
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECTION_TIMES = int(os.getenv("DB_CONNECTION_TIMES"))

# Database config for tests
DB_HOST_TEST = os.getenv("DB_HOST_TEST")
DB_PORT_TEST = os.getenv("DB_PORT_TEST")
DB_NAME_TEST = os.getenv("DB_NAME_TEST")
DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_PASSWORD_TEST = os.getenv("DB_PASSWORD_TEST")

# Auth token key config
TOKEN_SECRET = os.getenv("TOKEN_SECRET_KEY")

# Server settings
SERVER_PORT = int(os.getenv("SERVER_PORT"))
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PROTOCOL = os.getenv("SERVER_PROTOCOL")

# Debug status
DEBUG = bool(os.getenv("DEBUG"))

# url for connection to DB
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

FRONTEND_HOST = os.getenv("FRONTEND_HOST")
FRONTEND_PORT = os.getenv("FRONTEND_PORT")
FRONTEND_PROTOCOL = os.getenv("FRONTEND_PROTOCOL")

FRONTEND_URL = f'{FRONTEND_PROTOCOL}://{FRONTEND_HOST}:{FRONTEND_PORT}'
print(f'{FRONTEND_URL=}')
