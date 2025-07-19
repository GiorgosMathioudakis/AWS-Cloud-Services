import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    statusCode = 200
    username = event['username']
    passwordHash = event['passwordHash']
    email = event['email']
    table_name = "Users"
    
    # Select your DynamoDB table
    table = dynamodb.Table(table_name)
    
    response = table.scan(
        FilterExpression=Attr('username').eq(username) & Attr('email').eq(email)
    )

    if response['Items']:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Username or email already exists."),
            'hasDuplicate': "NoPass"
        }
    
    # If no duplicate, return success data
    return {
        'statusCode': 200,
        'username' : username,
        'email' : email,
        'passwordHash' : passwordHash , 
        'highscore' : 0
    }