#!/usr/bin/python
# import time
# from random import randint
# import random
import boto3
import uuid
import logging
# from dynamodb import DynamoDB

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    '''
    Insert alert data into DynamoDB
    '''
    try:
        logger.info("Processing event ::")
        logger.info(event)
        response = {"foo" : "bar"}
        
        client = boto3.client('dynamodb')

        table_name = event['table_name'] if 'table_name' in event else 'vib-mon-sls-device-readings-dev'
        records = event['Records']
        for row in records:
            payload = row['dynamodb']['NewImage']
            payload['uid'] = {"S" : str(uuid.uuid4())}
      
            response = client.put_item(
                TableName = table_name,
                Item = payload)
      
        return response
    except Exception as exp:
        logger.exception("Exception occured in lambda func %s", exp)