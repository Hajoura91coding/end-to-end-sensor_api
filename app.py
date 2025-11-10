from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
from src.sensor import VisitSensor

app = FastAPI()
sensor = VisitSensor(avg_visit=1500, std_visit=150)


@app.get("/")
def visits(
    year: int, month: int, day: int, hour: int, sensor_id: int | None = None
) -> JSONResponse:
    try:
        business_datetime = datetime(year, month, day, hour)
    except TypeError as e:
        return JSONResponse(status_code=404, content="Enter a valid date")
    visit_counts = sensor.get_visit_count(business_datetime)

    if visit_counts < 0:
        return JSONResponse(
            status_code=404, content="The store was closed try another date"
        )

    return JSONResponse(status_code=200, content=visit_counts)
