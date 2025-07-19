import json
import re

def lambda_handler(event, context):
    print(event)
    username = event['username']
    email = event['email']
    passwordHash = event['passwordHash']
    
    if(validate_uoc_email(email) & validate_username(username)):
        return{
            'statusCode':200,
            'username' : username,
            'email' : email,
            'passwordHash' : passwordHash
        }
    else:
        return{
            'statusCode':400
        }



def validate_uoc_email(email):
    print(email)
    """Validate if the email ends with '.uoc.gr'."""
    pattern = r'.*\.uoc\.gr$'  # .* matches any characters before .uoc.gr
    if re.match(pattern, email):
        return True
    else:
        print("email invalid")
        return False
    
def validate_username(username):
    """Validate if the username is greater than 4 characters."""
    if len(username) > 4:
        return True
    else:
        print("Username invalid")
        return False