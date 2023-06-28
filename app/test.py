import json
from lambda_function import lambda_handler

def main():
    """
    Testet die Lambda Funktion lokal.
    """

    # Testdaten definieren
    test_event = {
        "pathParameters": {
            "from_station": "FF",
            "to_station": "BLS"
        }
    }
    test_context = None

    # Lambda-Funktion aufrufen
    result = lambda_handler(test_event, test_context)

    # Ergebnis ausgeben
    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
