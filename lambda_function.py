import json
import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactFormSubmissions1')
ses = boto3.client('ses')
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
        id = str(uuid.uuid4())
        # Insert into DynamoDB
        response = table.put_item(
            Item={
                'id': id,
                'timestamp': timestamp,
                'name': name,
                'email': email,
                'message': message
            }
        )

        print("DynamoDB response:", response)  # Log the DynamoDB response
        
        send_email_notification(name, email, message)
        
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
    
def send_email_notification(name, email, message):
    SENDER = "sreenikethaathreya@gmail.com"
    RECIPIENT = email
    SUBJECT = "Thank you for your message"
    BODY_TEXT = f"""
    Dear {name},

    Thank you for contacting us. We have received your message and will get back to you soon.

    Your message:
    {message}

    Best regards,
    Sreeniketh Aathreya
    """
    
    BODY_HTML = f"""
    <html>
    <head></head>
    <body>
    <h2>Thank you for your message</h2>
    <p>Dear {name},</p>
    <p>Thank you for contacting us. We have received your message and will get back to you soon.</p>
    <h3>Your message:</h3>
    <p>{message}</p>
    <p>Best regards,<br>Sreeniketh Aathreya</p>
    </body>
    </html>
    """
    
    try:
        response = ses.send_email(
            Destination={'ToAddresses': [RECIPIENT]},
            Message={
                'Body': {
                    'Html': {'Data': BODY_HTML},
                    'Text': {'Data': BODY_TEXT},
                },
                'Subject': {'Data': SUBJECT},
            },
            Source=SENDER
        )
    except Exception as e:
        print("Error sending email:", str(e))
        raise e
    