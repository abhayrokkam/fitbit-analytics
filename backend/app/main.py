from fastapi import FastAPI, HTTPException
from datetime import date, timedelta
from . import crud, models

app = FastAPI()

@app.get("/data/{user_id}/{metric}", response_model=models.MetricResponse)
def read_data(user_id: str, metric: str, start_date: date = None, end_date: date = None):
    """  
    """
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - timedelta(days=7)

    if metric != 'heart_rate':
        raise HTTPException(status_code=404, detail="Metric not found. Only 'heart_rate' is supported.")
    
    data = crud.get_metric_data(start_date=start_date, end_date=end_date, metric=metric) 
    if not data:
        raise HTTPException(status_code=404, detail="No data found for the given parameters.")

    return {
        "user_id": user_id,
        "metric": metric,
        "data": data
    }