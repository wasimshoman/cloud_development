import json
import boto3

# Connect to DynamoDB and point to our notes table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def handler(event, context):
    # scan() reads every item in the table
    result = table.scan()
    notes = result['Items']

    # Return all notes as a JSON array
    return {
        'statusCode': 200,
        'body': json.dumps(notes)
    }
