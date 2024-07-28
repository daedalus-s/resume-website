import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactFormSubmissions1')

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))  # Log the entire event
        
        # Parse the incoming JSON
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        
        # Extract form data
        name = body['name']
        email = body['email']
        message = body['message']
        
        # Generate a timestamp
        timestamp = datetime.now().isoformat()
        
        # Insert into DynamoDB
        response = table.put_item(
            Item={
                'timestamp': timestamp,
                'name': name,
                'email': email,
                'message': message
            }
        )
        
        print("DynamoDB response:", response)  # Log the DynamoDB response
        
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent successfully!'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Replace with your domain in production
            }
        }
    except Exception as e:
        print("Error:", str(e))  # Log any errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Replace with your domain in production
            }
        }