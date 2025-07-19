import boto3
import json

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# DynamoDB table name
DYNAMODB_TABLE = 'UserAllocations'

def lambda_handler(event, context):
    # Get the DynamoDB table
    table = dynamodb.Table(DYNAMODB_TABLE)

    # Process each record from the SQS event
    for record in event['Records']:
        # Parse the SQS message body
        body = json.loads(record['body'])

        # Extract data
        allocation_vector = body['allocation_vector']
        public_ip = body['public_ip']

        # Write to DynamoDB
        table.put_item(
            Item={
                'PublicIP': public_ip,
                'AllocationVector': allocation_vector
            }
        )

        print(f"Processed and inserted: {body}")

    return {'statusCode': 200, 'body': 'Processed messages successfully'}
