import json
import boto3
import os

# Initialize SQS client
sqs = boto3.client('sqs')

# Environment variables for the SQS queue URLs
SQS_QUEUE_1_URL = "https://sqs.us-east-1.amazonaws.com/089781853604/SQS_1"
SQS_QUEUE_2_URL =  "https://sqs.us-east-1.amazonaws.com/089781853604/SQS_2"

def lambda_handler(event, context):
    # Parse the request body
    body = json.loads(event['body'])
    username = body['username']
    passwordHash = body['passwordHash']
    new_score = body['score']
    
    # Message to enqueue
    message = {
        'username': username,
        'passwordHash': passwordHash,
        'score': new_score
    }
    
    # Send messages to both SQS Queue 1 and Queue 2
    sqs.send_message(QueueUrl=SQS_QUEUE_1_URL, MessageBody=json.dumps(message))
    sqs.send_message(QueueUrl=SQS_QUEUE_2_URL, MessageBody=json.dumps(message))
    
    # Return success response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Score data enqueued successfully'})
    }
