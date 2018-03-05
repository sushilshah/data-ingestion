import boto3
import json
import logging

from decimal import *
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # table_name = 'device_status'
        table_name = 'vib-mon-sls-device-dev'

        # response = update_event(event, table_name)
        # response = update_event_as_is(event, table_name)
        response = []
        for item in event:
            logger.info("Event %s", item)
            resp = update_event_as_is(item, table_name)
            response.append(resp)
        # response = "Success invoking Lambda"
        return response
    except Exception as exp:
        logger.exception(exp)

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

    item['updated'] = int(time.time())
    for key in item:
        expression_str += key + '= :' + key + ', '
        # Quick and shameful Hack
        if(type(item[key]) is float):
            # eav[':' + key] = Decimal(item[key])
            eav[':' + key] = str(item[key])
        else:
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
        ReturnValues='UPDATED_NEW',
    )
    logger.info("Response %s", response)
    return response

def insert_item(item, table_name):
    """Insert an item to table"""
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    # if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    return response
    