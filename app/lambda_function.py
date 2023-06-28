import math
import csv
import json

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Berechnet die Distanz zwischen zwei Punkten anhand von 
    Laengen- und Breitengrad.
    """
    
    # Umrechnung in Radianten
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine-Formel zur Berechnung
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius der Erde in Kilometern

    return round(distance)

def read_csv(filename):
    """
    Liest aus einer csv Datei den DS100 Code (ds100), 
    den Namen des Bahnhofs (name) sowie den Laengen- (longitude) und 
    Breitengrad (latitute) ein und fügt diese Daten in einem dict zusammen.
    """
    
    data = []

    # Öffnet die csv datei
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Liest die Daten DS100 code, Name, Laengen- und Breitengrad aus der csv ein
        for row in reader:
            ds100 = row['DS100']
            name = row['NAME']
            latitude = float(row['Laenge'].replace(',', '.'))
            longitude = float(row['Breite'].replace(',', '.'))

            # Fügt die Daten in ein dict zusammen
            data.append({'DS100': ds100, 'NAME': name, 'Latitude': latitude, 'Longitude': longitude})

    return data

def lambda_handler(event, context):
    """
    Die Lambda Funktion führt nun die Logik anhand der angegebenen Daten aus.
    Die Bahnhöfe werden vom benutzer im Pfad der API mittels des DS100 codes
    angegeben.
    z.B.: https://x0rdzwzdc0.execute-api.eu-central-1.amazonaws.com/api/v1/distance/FALZ/KB
    wobei FALZ für den Startbahnhof (Alzey) und KB für den Zielbahnhof (Bonn) steht.
    """
    
    # extrahiert den Wert des Pfadparameters aus dem API request
    from_station = event['pathParameters']['from_station']
    to_station = event['pathParameters']['to_station']

    filename = 'D_Bahnhof_2020_alle.csv'
    csv_data = read_csv(filename)

    # sucht nach dem passenden Bahnhof mit dem DS100 code und ruft die dazugehörigen Daten ab
    from_station_data = next((item for item in csv_data if item['DS100'] == from_station), None)
    to_station_data = next((item for item in csv_data if item['DS100'] == to_station), None)

    # berechnet die Distanz zwischen d. Bahnhöfen
    if from_station_data and to_station_data:
        distance = calculate_distance(from_station_data['Latitude'], from_station_data['Longitude'],
                                      to_station_data['Latitude'], to_station_data['Longitude'])
        response = {
            "from": from_station_data['NAME'],
            "to": to_station_data['NAME'],
            "distance": distance,
            "unit": "km"
        }
    else:
        response = {
            "message": "One or both stations not found"
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }