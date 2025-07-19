import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Parse the body from the event if it's a POST request through API Gateway
    if 'body' in event:
        body = json.loads(event['body'])  # Parse the incoming JSON body
        username = body['username']
        passwordHash = body['passwordHash']
    else:
        username = event['username'] # Fallback in case the body is passed differently
        passwordHash = event['passwordHash']
        

    # Check if the username and passwordHash exist
    exists, highscore, email = check_user_exists(username, passwordHash)
    print(exists)
    if (exists == "true"):
        return {
            'statusCode': 200,
            'body': json.dumps({
                'username': username,
                'email': email,
                'highscore': highscore
            })
        }
    
    
    return {
        'statusCode': 400
    }
    
    

def check_user_exists(username, passwordHash):
    """Check if the username or email already exists in the DynamoDB table."""
    highscore = 0
    # Select your DynamoDB table
    table = dynamodb.Table("Users")
    
    # Query for the username
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    
    print(response)
    
    # Check if any items match
    if response['Items']:
        user_data = response['Items'][0]
        print(user_data.get('passwordHash'))
        print(passwordHash)
        
        # Validate the passwordHash
        if (user_data.get('passwordHash') == passwordHash):
            highscore = int(user_data.get('highscore', 0))  # Default highscore to 0 if not found
            email = user_data.get('email', "No email provided")  # Default email message
            return "true", highscore, email

    # If no match, return failure
    return "false", 0, ""