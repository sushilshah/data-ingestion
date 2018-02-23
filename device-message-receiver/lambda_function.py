import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # table_name = 'device_status'
        table_name = 'vib-mon-sls-device-dev'

        # response = update_event(event, table_name)
        response = update_event_as_is(event, table_name)
        return response
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
          '#cycle_val' : 'cycle',
          '#status_val' : 'status',
          '#load_val' : 'load',
        },
        ExpressionAttributeValues={
          ':current': data['current'],
          ':cycle': data['cycle'],
          ':updated': data['updated'],
          ':status': data['status'],
          ':temperature': data['temperature'],
          ':voltage' : data['voltage'],
          ':speed_rpm' : data['speed_rpm'],
          ':power' : data['power'],
          ':load' : data['load'],
          ':humidity': data['humidity'],
          ':s1': data['s1'],
          ':s2': data['s2'],
          ':s3' : data['s3'],
          ':s4' : data['s4'],
        },
        UpdateExpression='SET #current_val = :current, '
                         '#cycle_val = :cycle, '
                         '#status_val = :status, '
                         'temperature = :temperature, '
                         'voltage = :voltage, '
                         'speed_rpm = :speed_rpm, '
                         'power = :power, '
                         '#load_val = :load, '
                         'humidity = :humidity, '
                         's1 = :s1, '
                         's2 = :s2, '
                         's3 = :s3, '
                         's4 = :s4, '
                         'updated = :updated',
        ReturnValues='ALL_NEW',
    )
    
    print(response)
    return response

def update_event_as_is(item, table_name):
    data = {
            "id" : "namah",
            "humidity" : 10,
            "x" : 12,
            "y": 11
           }
    expression_str = ''
    eav = {}
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table(table_name)
    # id_key = 'namah'
    id_key = item['id']
    del item['id']

    for key in item:
        expression_str += key + '= :' + key + ', '
        eav[':' + key] = item[key]
    updateExp = 'SET ' + expression_str.strip(', ')
    # key = data['id']
    # response = table.update_item(Key=key,   Item=data)
    response = table.update_item(
        Key={
            'id': id_key
        },
        ExpressionAttributeValues=eav,
        UpdateExpression=updateExp,
        ReturnValues='ALL_NEW',
    )
    return response

def insert_item(item, table_name):
    """Insert an item to table"""
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    # if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    return response
    