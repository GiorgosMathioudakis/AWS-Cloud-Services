import json
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Define the table name
    table_name = "Leaderboard"
    
    # Scan the table to get all items
    response = dynamodb.scan(
        TableName=table_name
    )
    
    # Extract items from the response
    items = response.get('Items', [])
    
    # Create a list to hold the formatted leaderboard
    leaderboard = []
    
    # Iterate over the items and format them
    for item in items:
        leaderboard.append({
            'username': item['username']['S'],  # Extract 'username' (String type)
            'score': item['score']['N']         # Extract 'score' (Number type)
        })
    
    # Return the response in the required format
    return {
        'statusCode': 200,
        'body': json.dumps(leaderboard)
    }
