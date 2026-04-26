import json
import boto3

# Connect to DynamoDB and point to our notes table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def handler(event, context):
    # Get the note id from the URL and the new values from the request body
    note_id = event['pathParameters']['id']
    body = json.loads(event['body'])

    # Update only the title and content — we don't touch the id or createdAt
    # The UpdateExpression works like SQL SET — it tells DynamoDB which fields to change
    table.update_item(
        Key={'id': note_id},
        UpdateExpression='SET title = :title, content = :content',
        ExpressionAttributeValues={
            ':title': body['title'],
            ':content': body['content']
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Note updated'})
    }
