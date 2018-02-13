import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        table_name = 'device_status'
        data = update_event(event, table_name)
        return data
    except Exception as exp:
        logger.exception(exp)

def update_event(item, table_name):
    data = {
        "coordinates": {
            "Latitude": "12.9716",
            "Longitude": "77.5946"
        },
        "current": 19,
        "cycle": "9",
        "humidity": 86,
        "id": "namah",
        "load": 480,
        "origin": "cmapssdata",
        "power": "55MW",
        "s1": "18.67",
        "s10": "1.30",
        "s11": "47.03",
        "s2": "41.71",
        "s3": "1591.24",
        "s4": "1400.46",
        "s5": "14.62",
        "s6": "21.61",
        "s7": "553.59",
        "s8": "2388.05",
        "s9": "9051.70",
        "setting1": "-0.0033",
        "setting2": "0.0001",
        "setting3": "100.0",
        "speed_rpm": 3000,
        "status": "Halted",
        "temperature": 172,
        "updated": 1518179095,
        "voltage": "10.5 KV"
    }
    data = item if item else data
    
    table = dynamodb.Table(table_name)
    # table_name = 'device_status'
    if not 'id' in data:
        raise ValueError('Mandatory value id not found in the event %s', item)
    key = data['id']
    response = table.update_item(
        Key={
            'id': key
        },
        ExpressionAttributeNames={
          '#current_val': 'current',
          '#cycle_val' : 'cycle'
        },
        ExpressionAttributeValues={
          ':current': data['current'],
          ':cycle': data['cycle'],
          ':updated': data['updated'],
        },
        UpdateExpression='SET #current_val = :current, '
                         '#cycle_val = :cycle, '
                         'updated = :updated',
        ReturnValues='ALL_NEW',
    )
    
    print(response)
    return response

def insert_item(item, table_name):
    """Insert an item to table"""
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    # if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    return response
    