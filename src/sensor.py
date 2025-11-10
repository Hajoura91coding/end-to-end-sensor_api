from datetime import datetime
import numpy as np


class VisitSensor:
    """
    Simulates a sensor at the entrance of a mall.
    Returns the number of visitors per hour.
    """

    def __init__(
            self,
            avg_visit: int,
            std_visit: int,
            perc_break: float = 0.015,
            perc_malfunction: float = 0.035
    ) -> None:
        """Initialize sensor with daily traffic parameters"""
        self.avg_visit = avg_visit
        self.std_visit = std_visit
        self.perc_break = perc_break
        self.perc_malfunction = perc_malfunction

    def get_visit_count(self, business_date: datetime) -> float:
        """
        Return the number of visitors for a specific hour.
        Returns -1 if store is closed, 0 if sensor is broken.
        """
        # Unique seed for this specific hour (data generation)
        seed_visits = business_date.toordinal() * 24 + business_date.hour

        # Different seed for malfunction check (to decorrelate)
        seed_malfunction = seed_visits + 1000000

        # Check if sensor is broken
        np.random.seed(seed=seed_malfunction)
        proba_malfunction = np.random.random()

        if proba_malfunction < self.perc_break:
            return 0  # Sensor broken

        # Check day of week
        week_day = business_date.weekday()

        # Store closed on Sunday
        if week_day == 6:
            return -1

        # Generate visit count with reproducible seed
        np.random.seed(seed=seed_visits)
        daily_visit = np.random.normal(self.avg_visit, self.std_visit)

        # Traffic multipliers
        if week_day == 2:  # Wednesday
            daily_visit *= 1.10
        if week_day == 4:  # Friday
            daily_visit *= 1.25
        if week_day == 5:  # Saturday
            daily_visit *= 1.35

        # Convert to hourly
        hourly_visit = daily_visit / 24

        # Apply malfunction (20% reading)
        if proba_malfunction < self.perc_malfunction:
            hourly_visit *= 0.2

        return max(0, hourly_visit)


if __name__ == "__main__":
    sensor = VisitSensor(1500, 150)

    # Test specific datetime
    test_datetime = datetime(2024, 10, 25, 14)
    print(f"Visits at {test_datetime}: {sensor.get_visit_count(test_datetime):.2f}")

    # Test over several hours
    for hour in range(8, 18):
        dt = datetime(2024, 10, 25, hour)
        visits = sensor.get_visit_count(dt)
        print(f"{dt.strftime('%Y-%m-%d %H:00')} - Visits: {visits:.2f}")