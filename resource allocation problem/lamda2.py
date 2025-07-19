import boto3
import json
import requests


# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# DynamoDB table name
DYNAMODB_TABLE = 'UserAllocations'

# Cloud Provider URL
CLOUD_PROVIDER_URL = 'http://184.73.242.139:5000/receive-matrix'

def lambda_handler(event, context):
    # Get the DynamoDB table
    table = dynamodb.Table(DYNAMODB_TABLE)

    # Scan the table to retrieve all items
    response = table.scan()
    items = response['Items']

    # Check if all 3 items are present
    if len(items) < 3:
        print(f"Not enough allocations yet. Current count: {len(items)}")
        return {"statusCode": 200, "body": "Not enough allocations yet."}

    # Sort items by user or IP (assuming public IP order or user-specific key)
    items.sort(key=lambda x: x['PublicIP'])

    # Create allocation matrix and IP list
    allocation_matrix = []
    ips = []
    for item in items:
        allocation_matrix.append(item['AllocationVector'])
        ips.append(item['PublicIP'])

    # Prepare payload for Cloud Provider
    payload = {
        "allocation_matrix": allocation_matrix,
        "ips": ips
    }

    # Send data to Cloud Provider
    try:
        response = requests.post(CLOUD_PROVIDER_URL, json=payload)
        print(f"Response from Cloud Provider: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending data to Cloud Provider: {e}")
        return {"statusCode": 500, "body": f"Error sending data to Cloud Provider: {e}"}

    return {"statusCode": 200, "body": "Allocation matrix sent successfully."}
