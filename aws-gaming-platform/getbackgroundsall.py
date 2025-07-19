import json
import boto3
import os

# Initialize S3 client
s3 = boto3.client('s3')

# The name of your S3 bucket (retrieved from environment variable)
BUCKET_NAME = "backgroundbacket"

def lambda_handler(event, context):
    print(f"Using bucket: {BUCKET_NAME}")  # Log the bucket name for debugging
    
    try:
        # List all objects with the prefix "backgrounds/"
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix='backgrounds/'  # Only list objects in the 'backgrounds/' directory
        )
        
        # Check if any objects were found
        if 'Contents' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No backgrounds found'})
            }
        
        # Build the list of backgrounds to return
        backgrounds = []
        for obj in response['Contents']:
            backgrounds.append({
                'Key': obj['Key'],  # The file name
                'Size': obj['Size']  # The size in bytes
            })
        
        # Return the list of backgrounds
        return {
            'statusCode': 200,
            'body': json.dumps(backgrounds)
        }
    
    except Exception as e:
        print(f"Error retrieving backgrounds: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
