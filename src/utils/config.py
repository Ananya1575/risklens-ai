import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DATA_DIR = "data"
MODELS_DIR = "models"
SQL_DB_PATH = "sql/credit_risk.db"

TARGET_COLUMN = "TARGET"
RANDOM_STATE = 42
TEST_SIZE = 0.2