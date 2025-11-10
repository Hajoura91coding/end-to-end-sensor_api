from fastapi import FastAPI, HTTPException
from datetime import datetime
from src.sensor import VisitSensor

app = FastAPI()
sensor = VisitSensor(avg_visit=1500, std_visit=150)


@app.get("/")
def get_visits(
        year: int,
        month: int,
        day: int,
        hour: int,
        sensor_id: int | None = None
) -> dict:
    """
    Get visit count for a specific datetime.

    Args:
        year, month, day, hour: datetime components
        sensor_id: optional sensor identifier (not used yet)

    Returns:
        JSON with visit count or error
    """
    # Validate datetime
    try:
        business_datetime = datetime(year, month, day, hour)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date: {str(e)}")

    # Check if date is in the future
    if business_datetime > datetime.now():
        raise HTTPException(status_code=400, detail="Cannot query future dates")

    # Get visit count
    visit_count = sensor.get_visit_count(business_datetime)

    # Handle closed store (Sunday)
    if visit_count < 0:
        raise HTTPException(status_code=404, detail="Store was closed at this time")

    return {
        "datetime": business_datetime.isoformat(),
        "visit_count": round(visit_count, 2),
        "sensor_id": sensor_id,
        "status": "ok" if visit_count > 0 else "sensor_broken"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}