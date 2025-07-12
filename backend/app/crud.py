import os
from dotenv import load_dotenv
from datetime import date, datetime

from modules.logging_config import setup_logger
from modules.db_connection import get_db_connection

# -------------------- Setup --------------------

load_dotenv()
logger = setup_logger(__name__)

# -------------------- Get --------------------

def get_metric_data(start_date: date, end_date: date, metric: str):
    query = """
        SELECT time, value from raw_data
        WHERE client_id = %s AND metric = %s AND time >= %s AND time < %s
        ORDER BY time;
    """
    results = []
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Adjust end_date to cover full day
            end_datetime = datetime.combine(end_date, datetime.max.time())

            try: 
                client_id = os.getenv('CLIENT_ID')
                cursor.execute(query, 
                               (client_id, metric, start_date, end_datetime))
                results = cursor.fetchall()
            except Exception as e:
                logger.error(f"[ERROR] There was an error trying to get metric data (crud.py): {e}")
                raise e
            
    if(len(results) == 0):
        logger.warning(f"[WARNING] None of the rows were fetched during get metric data (crud.py)")
        
    return [{"time": row[0], "value": row[1]} for row in results]