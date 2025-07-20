import os
import json
from dotenv import load_dotenv

import pandas as pd
from datetime import timedelta, date

import wearipedia

from modules.logging_config import setup_logger
from modules.db_connection import get_db_connection

# -------------------- Setup --------------------

load_dotenv()
logger = setup_logger(__name__)

INGESTION_STATE_DIR = "./data/ingestion_state/"
LAST_RUN_FILE = os.path.join(INGESTION_STATE_DIR, "last_run.json")

# -------------------- Save-Fetch Date --------------------

def save_and_fetch_date() -> str:
    try:
        os.makedirs(INGESTION_STATE_DIR, exist_ok=True)

        filepath = LAST_RUN_FILE
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')

        # Write today's date
        output_data = {"date": today_date.strftime('%Y-%m-%d')}
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=4)
        logger.info(f"[INFO] Data processed for date: {yesterday_date_str}")

        # Return yesterday's date
        return yesterday_date_str
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error with saving-and-fetching dates: {e}")
        raise e

# -------------------- Main --------------------

def main():
    # Database Connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Save-Fetch Date
    yesterday_date = save_and_fetch_date()

    # Fitbit Config
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
    SYNTHETIC = os.getenv("SYNTHETIC", "")

    device = wearipedia.get_device('fitbit/fitbit_charge_6')
    if not SYNTHETIC:
        device.authenticate(ACCESS_TOKEN)

    params = {
        "start_date": yesterday_date,
        "end_date": yesterday_date
    }

    heart_rate_data = device.get_data("intraday_heart_rate", params)

    # Traversal and Ingestion
    for daily_data in heart_rate_data:
        day_record = daily_data['heart_rate_day'][0]
        date_str = day_record['activities-heart'][0]['dateTime']
        dataset = day_record['activities-heart-intraday']['dataset']
        logger.info(f"[INFO] Starting for date: {date_str}")

        for entry in dataset:
            time_str = entry['time']
            metric_str = 'heart_rate'
            value = float(entry['value'])
            timestamp = pd.to_datetime(f"{date_str} {time_str}").tz_localize('UTC')

            cursor.execute(
                """
                INSERT INTO raw_data (client_id, time, metric, value)
                VALUES (%s, %s, %s, %s)
                """,
                (CLIENT_ID, timestamp, metric_str, value)
            )

    logger.info("[INFO] Heart rate data ingestion complete")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()