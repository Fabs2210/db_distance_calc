Python script for an API that calculates the distance between two train stations in Germany.

API was built with AWS API Gateway.
Routes: /api, /v1, /distance, /{from_station}, /{to_station} (GET)

Integrated with a lambda function (see lambda_function.py) that reads from a csv.
Alternative version was built that reads from a DynamoDB database.
No authorization needed.

Use: curl "https://x0rdzwzdc0.execute-api.eu-central-1.amazonaws.com/api/v1/distance/{from_station}/{to_station}".
The parameters have to be replaced by a valid DS100 code for the train stations.
