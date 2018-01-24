import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('lambda')
    # TODO 
    response = client.invoke(
        FunctionName='insert-alert',
        InvocationType='Event',
        Payload=json.dumps({"test" : "payload"})
    )
    return 'Hello from Lambda'
