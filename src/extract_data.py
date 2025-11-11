
import sys
import datetime
import requests


def get_public_api(url: str) -> dict:
    """
    get public api
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error public API: {e}")
        return None

def get_sensor_api(year:int, month:int, day:int, hour:int)-> dict:
    """
    get sensor api to extract data
    """
    base_url = "http://127.0.0.1:8000/"
    params ={
        "year": year,
        "month": month,
        "day": day,
        "hour": hour
    }
    try:
        r= requests.get(base_url, params=params)
        if r.status_code != 200:
            print(f"Error API (status {r.status_code}): {r.json()}")
            return None
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error network: {e}")
        return None


if __name__ == "__main__":
    print("Hello world!")
    if sys.argv[1]:
        param = sys.argv[1]
        print(param)
    try:
        date_obj = datetime.datetime.strptime(param, "%Y-%m-%d")
        print(f"Date valide: {date_obj.strftime('%Y-%m-%d')}")
    except ValueError:
        print("Please enter a valid date, expected format: YYYY-MM-DD")
        sys.exit(1)

    # Extraction des composents de la date (en int)
    year, month, day = [int(v) for v in param.split("-")]

    # Partie D: test API publique
    print("\n Test Api publique")
    public_data = get_public_api("https://api.agify.io?name=agar")
    if public_data:
        print(f"API publique OK : {public_data.get('age')}")
    else:
        print("Echec API publique")
    # Partie E: test api capteurs
    sensor_data = get_sensor_api(year, month, day, hour=14)
    if sensor_data:
        print(f"API capteurs OK")
        print(f"Data\Heure: {sensor_data.get('datetime')}")
        print(f"Visites: {sensor_data.get('visit_count')}")
    else:
        print("Echec API capteurs")
