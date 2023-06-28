"""
Der selbe Code wie "lambda_function.py" nur das hier mit der DDB gearbeitet wird.
"""

import math
import json
import boto3

def calculate_distance(lat1, lon1, lat2, lon2):
    # Umrechnung in Radianten
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Formel zur Berechnung der Entfernung
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius der Erde in Kilometern

    return round(distance)

def read_dynamodb_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return items

def lambda_handler(event, context):
    from_station = event['pathParameters']['from_station']
    to_station = event['pathParameters']['to_station']

    table_name = 'db_table'
    dynamodb_data = read_dynamodb_table(table_name)

    from_station_data = next((item for item in dynamodb_data if item['DS100'] == from_station), None)
    to_station_data = next((item for item in dynamodb_data if item['DS100'] == to_station), None)

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
