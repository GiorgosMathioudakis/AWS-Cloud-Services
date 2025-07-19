import json
import boto3
import os

# Initialize DynamoDB and SNS clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# SNS topic ARN (passed as an environment variable)
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:089781853604:notifications"

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            message = json.loads(record['body'])
            
            # Validate message contents
            if 'username' not in message or 'score' not in message:
                print("Malformed message received. Missing 'username' or 'score'.")
                continue
            
            username = message['username']
            new_score = int(message['score'])
            
            # Fetch the user and their current highscore from the 'Users' table
            users_table = dynamodb.Table('Users')
            response = users_table.get_item(Key={'username': username})
            
            if 'Item' not in response:
                print(f"User {username} not found")
                continue
            
            user = response['Item']
            highscore = int(user.get('highscore', 0))  # Default to 0 if no highscore exists
            
            # If the new score is higher, update the highscore in Users table
            if new_score > highscore:
                users_table.update_item(
                    Key={'username': username},
                    UpdateExpression='SET highscore = :new_score',
                    ExpressionAttributeValues={':new_score': new_score}
                )
                
                # Send SNS notification for new highscore
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=f"New high score for {username}: {new_score}",
                    Subject="New High Score!"
                )
                print(f"New high score notification sent for {username}")
            else:
                print(f"New score ({new_score}) is not higher than current highscore ({highscore})")
    
    except Exception as e:
        print(f"Error processing record: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
