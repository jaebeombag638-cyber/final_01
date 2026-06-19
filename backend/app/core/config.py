import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")
TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "")
