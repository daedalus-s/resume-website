import json
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ContactMessages')
    
    body = json.loads(event['body'])
    
    message_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    item = {
        'MessageId': message_id,
        'Name': body['name'],
        'Email': body['email'],
        'Message': body['message'],
        'Timestamp': timestamp
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent successfully!'),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }