import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactFormSubmissions')

def lambda_handler(event, context):
    try:
        # Parse the incoming JSON from the API Gateway
        body = json.loads(event['body'])
        
        # Extract form data
        name = body['name']
        email = body['email']
        message = body['message']
        
        # Generate a unique ID and timestamp
        id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Insert into DynamoDB
        table.put_item(
            Item={
                'id': id,
                'name': name,
                'email': email,
                'message': message,
                'timestamp': timestamp
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Submission successful!'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://sreenikethaathreya.com'
            }
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing your request'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://sreenikethaathreya.com'
            }
        }