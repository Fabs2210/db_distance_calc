"""
Code der eine DDB Tabelle erstellt, Daten aus einem csv liest und diese im batch
in die DDB Tabelle schreibt.
"""

import csv
import boto3

def main():
    # Beispielaufruf der Funktionen
    filename = 'D_Bahnhof_2020_alle.csv'
    csv_data = read_csv(filename)

    table_name = 'db_table'
    create_dynamodb_table(table_name)
    batch_write_to_dynamodb(table_name, csv_data)

def create_dynamodb_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'DS100',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'DS100',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    table.wait_until_exists()
    print(f"DynamoDB table '{table_name}' has been created.")

def read_csv(filename):
    data = []
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        
        for row in reader:
            data.append(row)
    
    return data

def batch_write_to_dynamodb(table_name, items):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    total_items = len(items)
    count = 0
    
    with table.batch_writer() as batch:
        for item in items:
            ds100 = item['DS100']  # DS100-Code als Schlüsselwert
            batch.put_item(Item={**item, 'DS100': ds100})
            count += 1
            print(f"Inserted item {count}/{total_items}")

if __name__ == '__main__':
    main()

# man könnte verbessern:
# Provisioned Throughput erhöhen
# Verwenden von Parallelität
# Verwenden von Amazon DynamoDB Accelerator (DAX)