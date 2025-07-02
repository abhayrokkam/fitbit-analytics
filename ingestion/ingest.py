import os
import logging
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
logger = logging.getLogger(__name__)

# DB Connection
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

try:
    conn = psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_PASS,
                            port=DB_PORT)
    conn.autocommit = True
    cursor = conn.cursor() 
    logger.info(f"[INFO] Database connection successful!")
except Exception as e:
    logger.info(f"[ERROR] Database failed to connect: {e}")
    raise e

### POPULATE DB WITH COMMANDS

cursor.close()
conn.close()