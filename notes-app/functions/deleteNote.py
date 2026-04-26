import json
import boto3

# Connect to DynamoDB and point to our notes table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def handler(event, context):
    # Pull the note id from the URL
    note_id = event['pathParameters']['id']

    # Delete that item from DynamoDB 
    table.delete_item(Key={'id': note_id})

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Note deleted'})
    }
