import os
import json
from dotenv import load_dotenv

import pandas as pd
from datetime import datetime, timedelta

import wearipedia

from modules.logging_config import setup_logger
from modules.db_connection import get_db_connection

# -------------------- Setup --------------------

load_dotenv()
logger = setup_logger(__name__)

# -------------------- Save-Fetch Date --------------------

def save_and_fetch_date(filepath: str = "./data/ingestion_state/last_run.json") -> str:
    try:
        # Current date
        current_date = datetime.now()
        last_run_data = {'date': current_date.strftime('%Y-%m-%d')}

        # Save to file
        with open(filepath, 'w') as f:
            json.dump(last_run_data, f, indent=4)
        logger.info(f"[INFO] Save current date: {current_date}")

        # Previous date for return
        previous_date = (current_date-timedelta(days=1)).strftime('%Y-%m-%d')
        logger.debug(f"[DEBUG] Returning previous date: {previous_date}")
        return str(previous_date)
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error with saving-and-fetching dates")
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