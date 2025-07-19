import json
import boto3
from boto3.dynamodb.conditions import Attr


# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        username = message['username']
        passwordHash = message['passwordHash']
        new_score = int(message['score'])
        
        # Fetch the existing score from 'Leaderboard' table
        leaderboard_table = dynamodb.Table('Leaderboard')
        response = leaderboard_table.get_item(Key={'username': username})
        
        user_password_hash = get_user_password_hash(username)

        if not user_password_hash:
            print("prwti if")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'User not found!'})
            }
        
        # Step 2: Compare the passwordHash from the API request with the one from the Users table
        if user_password_hash != passwordHash:
            print("deuteri")
            return {
                'statusCode': 403,
                'body': json.dumps({'message': 'Invalid password!'})
            }
        
        current_score = 0
        if 'Item' in response:
            current_score = int(response['Item'].get('score', 0))
        
        # If the new score is higher, update the Leaderboard table
        if new_score > current_score:
            leaderboard_table.put_item(
                Item={'username': username, 'score': new_score}
            )
            print(f"Updated leaderboard with new score for {username}")
        else:
            print(f"New score ({new_score}) is not higher than current score ({current_score})")


def get_user_password_hash(username):
    """Retrieve the passwordHash from the 'Users' table for the given username."""
    table = dynamodb.Table('Users')
    
    try:
        # Query the Users table to get the item based on the username
        response = table.scan(
            FilterExpression=Attr('username').eq(username)
        )
        
        if response['Items']:
            user_data = response['Items'][0]
            return user_data.get('passwordHash')
        else:
            return None

    except Exception as e:
        print(f"Error querying Users table: {str(e)}")
        return None

