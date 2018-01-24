#!/usr/bin/python
import datetime
import time
from random import randint
import random
import logging
from dynamodb import DynamoDB

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    '''
    Insert alert data into DynamoDB
    '''
    table_name = event['table_name'] if 'table_name' in event else 'device_status'
    payload = create_mock_data(event)
    alerts = check_notify_alert(payload)
    payload['alerts'] = alerts
    payload['updated'] = int(time.time())
    response = DynamoDB().insert_item(table_name, payload)
    return response

def create_mock_data(base_obj):
    '''
    Create mock data
    
    :param base_obj (object):  {"id" : "xxxxxxUUIDxxxxxx", "name" : "device_name"}
    :returns: The mock data dict
    '''
    mock = dict()
    if not base_obj or not 'id' in base_obj:
        logger.info("Id not present in base obj, create pick random devices from mock")
        mock_devices = {'Sensor-300578' : '111',
                        'Sensor-300577' : '222',
                        'Sensor-300575' : '333',
                        'Sensor-300579' : '444',
                        'Sensor-195732' : '555'}
        device_name, device_id = random.choice(list(mock_devices.items()))
        mock['id'] = device_id
        mock['name'] = device_name

    '''Acceptable values:
    x_mms : 0-18, y_mms : 0-21, z_mms : 0-15, x_hz  : 5-47, y_hz  : 5-31, z_hz  : 5-51'''
    mock['x_mms'], mock['y_mms'], mock['z_mms'], mock['x_hz'], mock['y_hz'], mock['z_hz'] = \
    [randint(0,25), randint(0,30), randint(0,25), randint(5,60), randint(5,50), randint(5,60)]
    return mock

def check_notify_alert(d_reading_obj):
    '''
    Evaluate threshold based Alerts
    process alert threshold and invoke alert lambda

    Valid data point range:
    x_mms : 0-18, y_mms : 0-21, z_mms : 0-15, x_hz  : 5-47, y_hz  : 5-31, z_hz  : 5-51
    
    :param d_reading_obj (object): Sensor readings
    :returns: Dict of Alerts
    '''
    alerts = {}
    if not (0 <= d_reading_obj['x_mms'] <= 18):
        alerts['x_mms'] = d_reading_obj['x_mms']
    if not (0 <= d_reading_obj['y_mms'] <= 21):
        alerts['y_mms'] = d_reading_obj['y_mms']
    if not (0 <= d_reading_obj['z_mms'] <= 15):
        alerts['z_mms'] = d_reading_obj['z_mms']
    if not (5 <= d_reading_obj['x_hz'] <= 47):
        alerts['x_hz'] = d_reading_obj['x_hz']
    if not (5 <= d_reading_obj['y_hz'] <= 31):
        alerts['y_hz'] = d_reading_obj['y_hz']
    if not (5 <= d_reading_obj['z_hz'] <= 31):
        alerts['z_hz'] = d_reading_obj['z_hz']
    return alerts    
