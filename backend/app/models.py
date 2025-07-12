from pydantic import BaseModel
from datetime import datetime

class MetricDataPoint(BaseModel):
    """
    A generic model for a single time-series data point
    """
    time: datetime
    value: float

class MetricResponse(BaseModel):
    """
    A generic response model that can carry data for any metric
    """
    user_id: str
    metric: str
    data: list[MetricDataPoint]