import csv
import sys
import datetime
from pathlib import Path
from datetime import timedelta, date
import requests
import random
"""
“date”, “heure”, “id_du_capteur”, “id_du_magasin” 
(ou id_du_lieu/objet_dont_vous_récupérez_les_infos), “nombre de 
clics / visiteurs / items traités)”, “unité (Litres / Visisteurs / items / cl
"""
STORES = {
    "STORE_PARIS": {"id":"PARIS", "sensor_id":"SENSOR_PARIS_01"}
}

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

def extract_data_csv(date_param: str, store_id: str = "STORE_PARIS") :

    today_date = datetime.datetime.now()
    print(f"today_date: {today_date.strftime('%Y-%m-%d')}")
    year, month, day= [int(v) for v in date_param.split("-")]
    start_date = datetime.datetime(year, month, day)
    print(f"start_date: {start_date.strftime('%Y-%m-%d')}")
    current_date = start_date

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    data_by_month = {}

    #results = []
    while current_date <= today_date:
        month_key = current_date.strftime("%Y-%m")
        if month_key not in data_by_month:
            data_by_month[month_key] = []

        print(f"Current date: {current_date.strftime('%Y-%m-%d')}")
        data = get_sensor_api(
            year=current_date.year,
            month= current_date.month,
            day= current_date.day,
            hour= current_date.hour
            )
        if data:
            visit_count = data.get('visit_count', 0)

            sensor_id = STORES[store_id]["sensor_id"]
            unit = ("visiteurs")

            if random.random() < 0.05:
                sensor_id = None
                print(f"Corruption: id_capteur -> NULL")
            if random.random() < 0.03:
                unit = random.choice(["litres", "kilogrammes","watts","pixels"])
                print(f"CORRUPTION: unité -> {unit}")
            row = {
                "date": current_date.strftime('%Y-%m-%d'),
                "heure": current_date.hour,
                "id_capteur": sensor_id,
                "id_magasin":store_id,
                "nombre_visiteurs": round(visit_count,2),
                "unité":unit
            }
            data_by_month[month_key].append(row)
            print(f"{current_date.strftime('%Y-%m-%d %H:%M')} - Visites: {data.get('visit_count'):.2f}")
        else:
            print(f"{current_date.strftime('%Y-%m-%d %H:%M')} - Échec récupération")
        current_date += timedelta(hours=1)

    for month_key, rows in data_by_month.items():
        csv_filename = output_dir / f"{store_id}_{month_key}.csv"


        with open(csv_filename, 'w', newline='', encoding="utf-8") as f:
            fieldnames = ["date", "heure", "id_capteur", "id_magasin", "nombre_visiteurs", "unité"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            print(f"Fichier créer: {csv_filename} ({len(rows)})")
    print(f"\nTotal de données récupérées : {len(data_by_month)} fichiers CSV crées")
    return len(data_by_month)


if __name__ == "__main__":
    print("Hello world!")
    if len(sys.argv[1]) > 1:
        param = sys.argv[1]
        print(param)
    else:
        print("No provided date")
        sys.exit(1)
    try:
        date_obj = datetime.datetime.strptime(param, "%Y-%m-%d")
        print(f"Date valide: {date_obj.strftime('%Y-%m-%d')}")
    except ValueError:
        print("Please enter a valid date, expected format: YYYY-MM-DD")
        sys.exit(1)

    # Extraction des composantes de la date (en int)
    #year, month, day= [int(v) for v in param.split("-")]
    # # Partie D: test API publique
    # print("\n Test Api publique")
    # public_data = get_public_api("https://api.agify.io?name=agar")
    # if public_data:
    #     print(f"API publique OK : {public_data.get('age')}")
    # else:
    #     print("Echec API publique")
    # # Partie E: test api
    #
    # sensor_data = get_sensor_api(year, month, day, hour=14)
    # if sensor_data:
    #     print(f"API capteurs OK")
    #     print(f"Data\Heure: {sensor_data.get('datetime')}")
    #     print(f"Visites: {sensor_data.get('visit_count')}")
    # else:
    #     print("Echec API capteurs")
    nb_files = extract_data_csv(date_param=param, store_id="STORE_PARIS")
    print(f"\n {nb_files} fichiers CSV générés dans data/raw/")