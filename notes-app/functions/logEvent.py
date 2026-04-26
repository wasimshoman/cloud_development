import json

# This function is NOT triggered by an HTTP request like the others.
# It listens to EventBridge — whenever an event with source "notes-app"
# is fired, AWS automatically runs this function in the background.
def handler(event, context):
    print("Event received from EventBridge:")

    # Print the full event so we can see it in CloudWatch logs
    print(json.dumps(event, indent=2))

    return {'statusCode': 200}
