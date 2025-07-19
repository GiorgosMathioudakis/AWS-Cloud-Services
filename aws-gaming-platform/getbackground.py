import json
import boto3
import os
import base64

# Initialize S3 client
s3 = boto3.client('s3')

# Get the bucket name from environment variables
BUCKET_NAME = "backgroundbacket"

def lambda_handler(event, context):
    try:
        # Extract 'name' from query parameters
        name = event['queryStringParameters']['name']
        
        # Define the full key in S3 (with the 'backgrounds/' prefix)
        s3_key = f"backgrounds/{name}"
        
        # Fetch the object from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        
        # Read the file's binary data
        image_data = response['Body'].read()
        
        # Return the Base64-encoded image in the response (Note: Do not use json.dumps directly here)
        return {
            'headers': { 'Content-Type': 'image/jpeg' },
            'statusCode': 200,
            'body': base64.b64encode(image_data).decode('utf-8')
        }
    
    except s3.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': f'Image {name} not found'})
        }
    
    except Exception as e:
        print(f"Error fetching image {name}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
