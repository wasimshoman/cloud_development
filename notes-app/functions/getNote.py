import json
import boto3

# Connect to DynamoDB and point to our notes table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def handler(event, context):
    # The note id comes from the URL, e.g. /notes/abc-123
    note_id = event['pathParameters']['id']

    # Try to fetch that specific note from DynamoDB using its id
    result = table.get_item(Key={'id': note_id})

    # If DynamoDB didn't find anything, tell the caller it doesn't exist
    if 'Item' not in result:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Note not found'})
        }

    # Note was found — send it back
    return {
        'statusCode': 200,
        'body': json.dumps(result['Item'])
    }
