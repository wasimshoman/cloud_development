import json
import boto3
import uuid
from datetime import datetime

# Connect to DynamoDB and point to our notes table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def handler(event, context):
    # The request body comes in as a string, so we parse it into a Python dict
    body = json.loads(event['body'])

    # Generate a unique id for this note — every note needs one to be found later
    note_id = str(uuid.uuid4())

    # Save the note to DynamoDB with all its fields
    table.put_item(Item={
        'id': note_id,
        'title': body['title'],
        'content': body['content'],
        'createdAt': datetime.utcnow().isoformat()  # store when it was created
    })

    # Send back a 201 (meaning "created") with the new note's id
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Note created', 'id': note_id})
    }
