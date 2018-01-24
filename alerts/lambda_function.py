from dynamodb import DynamoDB

def lambda_handler(event, context):
    '''
    Insert alert data into DynamoDB
    '''
    # print(event)
    table_name = event['table_name'] if 'table_name' in event else 'alerts'
    if 'payload' in event:
        payload = event['payload']
    else:
        # payload = {'id' : 'mock_payload', 'alert' : 22}
        return "Mandatory Payload missing"
    response = DynamoDB().insert_item(table_name, payload)
    return response