import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection
from .logging_config import setup_logger

# -------------------- Setup --------------------

load_dotenv()
logger = setup_logger(__name__)

# -------------------- Database Connection --------------------

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        conn.autocommit = True
        logger.info("[INFO] Database connection successful")
        return conn
    except Exception as e:
        logger.error(f"[ERROR] Database connection failed: {e}")
        raise e