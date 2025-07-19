import json
import boto3

stepfunctions = boto3.client('stepfunctions')

STATE_MACHINE_ARN = "arn:aws:states:us-east-1:089781853604:stateMachine:MyStateMachine"


def lambda_handler(event, context):
    

    body = json.loads(event['body']) if 'body' in event else event
    action = body['action']
    username = body['username']
    passwordHash = body['passwordHash']
    if(action=="Register"):
        email = body['email']
    else:
        email = "empty"

    # Start the Step Functions state machine execution
    response = stepfunctions.start_sync_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps({
            'username': username,
            'email': email,
            'passwordHash' : passwordHash , 
            'action' : action
        })
    )
    
    print(response)
    
    
    if(action == "Login"):
        
        if(json.loads(response['output'])['statusCode']==200):
            body = json.loads(json.loads(response['output'])['body'])
            username = body['username']
            email = body['email']
            highscore = body['highscore']
            return {
                'statusCode': 200 ,
                'body': json.dumps({
                    'username' : username , 
                    'email' : email , 
                    'highscore' : highscore
                })
            }
        else:
            return{
                'statusCode' : 400
            }
            
    else:
        if(response['status']=="FAILED"):
            statusCode = 400
        else:
            statusCode = 200
        return {
            'statusCode': statusCode
        }
