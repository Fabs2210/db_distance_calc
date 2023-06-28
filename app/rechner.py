import csv
from math import radians, sin, cos, sqrt, atan2

def main():
    """
    Testet die Hauptlogik eines Entfernungsrechners zwischen zwei Bahnhöfen.
    Die Daten werden aus einer CSV-Datei gelesen.
    """

    # Aufruf der Funktion
    filename = 'D_Bahnhof_2020_alle.csv'
    csv_data = read_csv(filename)

    # Beispiel: Berechnung der Distanz zwischen den ersten beiden Bahnhöfen
    bahnhof1 = csv_data[0]
    bahnhof2 = csv_data[1]

    lat1 = bahnhof1['Breite']
    lon1 = bahnhof1['Laenge']
    lat2 = bahnhof2['Breite']
    lon2 = bahnhof2['Laenge']

    distance = calculate_distance(lat1, lon1, lat2, lon2)
    print(f'Die Distanz zwischen den Bahnhöfen {bahnhof1["NAME"]} und {bahnhof2["NAME"]} beträgt {distance:.2f} km.')

def read_csv(filename):
    data = []

    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            ds100 = row['DS100']
            name = row['NAME']
            laenge = float(row['Laenge'].replace(',', '.'))
            breite = float(row['Breite'].replace(',', '.'))

            data.append({'DS100': ds100, 'NAME': name, 'Laenge': laenge, 'Breite': breite})

    return data

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine-Formel verwendet, um die Distanz zwischen zwei Koordinatenpaaren zu berechnen
    R = 6371  # Radius der Erde in Kilometern

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

if __name__ == '__main__':
    main()
