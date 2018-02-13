#!/usr/bin/python
import time
from random import randint
import random
import logging
from dynamodb import DynamoDB
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    '''
    Insert alert data into DynamoDB
    '''
    try:
        logger.info("Processing event ::")
        logger.info(event)
        device = event
        table_name = event['table_name'] if 'table_name' in event else 'device_status'
        
        alerts = check_notify_alert(device)
        device['alerts'] = alerts
        device['updated'] = int(time.time())
        logger.info("payload for dynamodb insert::")
        logger.info(device)
        response = DynamoDB().insert_item(table_name, device)
        
        # for device in payload:
        # payload = create_mock_data(event)

        #     alerts = check_notify_alert(device)
        #     device['alerts'] = alerts
        #     device['updated'] = int(time.time())
        #     logger.info("payload for dynamodb insert::")
        #     logger.info(device)
        #     response = DynamoDB().insert_item(table_name, device)
        return response
    except Exception as exp:
        logger.exception("Exception occured in lambda func %s", exp)



def create_mock_data(base_obj):
    '''
    Create mock data
    
    :param base_obj (object):  {"id" : "xxxxxxUUIDxxxxxx", "name" : "device_name"}
    :returns: The mock data dict
    '''
    try:
        mock = dict()
        if not base_obj or not 'id' in base_obj:
            logger.info("Id not present in base obj, create pick random devices from mock")
            mock_devices = {'Sensor-300578' : '111',
                            'Sensor-300577' : '222',
                            'Sensor-300575' : '333',
                            'Sensor-300579' : '444',
                            'Sensor-195732' : '555'}
            # device_name, device_id = random.choice(list(mock_devices.items()))
            mock_devices_list = []
            for item in mock_devices:
                print(item, mock_devices[item])
                mock = dict()
                mock = mock_device()
                mock['id'] = mock_devices[item]
                mock['name'] = item
                mock_devices_list.append(mock)
        return mock_devices_list
    except Exception as exp:
        raise exp

def mock_device():
    mock = dict()
    '''Acceptable values:
    x_mms : 0-18, y_mms : 0-21, z_mms : 0-15, x_hz  : 5-47, y_hz  : 5-31, z_hz  : 5-51'''
    mock['x_mms'], mock['y_mms'], mock['z_mms'], mock['x_hz'], mock['y_hz'], mock['z_hz'] = \
    [randint(0,20), randint(0,23), randint(0,20), randint(5,50), randint(5,35), randint(5,53)]
        
    device_statuses = ['Running', 'Halted', 'Idle']
    device_status = random.choice(device_statuses)
    coordinates = {"Latitude" : '12.9716',
                  "Longitude" : '77.5946'}
    load = 480
    speed_rpm = 3000
    power = '55MW'
    current = randint(0,50)
    voltage = '10.5 KV'
    temperature = randint(0,500) 
    humidity = randint(0,100)
    mock['current'], mock['voltage'], mock['temperature'], mock['humidity'], \
    mock['coordinates'], mock['load'], mock['speed_rpm'], mock['power'], mock['status'] =\
     [current, voltage, temperature, humidity, coordinates, load, speed_rpm, power, device_status ]
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
    '''
        TODO: Add Alert and Danger thresholds
        from  http://ijettcs.org/Volume2Issue6/IJETTCS-2013-12-24-089.pdf
    '''
    try:
        alerts = {}
        if 'x_mms' in d_reading_obj and not (0 <= d_reading_obj['x_mms'] <= 18):
            alerts['x_mms'] = d_reading_obj['x_mms']
        if 'y_mms' in d_reading_obj and not (0 <= d_reading_obj['y_mms'] <= 21):
            alerts['y_mms'] = d_reading_obj['y_mms']
        if 'z_mms' in d_reading_obj and not (0 <= d_reading_obj['z_mms'] <= 15):
            alerts['z_mms'] = d_reading_obj['z_mms']
        if 'x_hz' in d_reading_obj and  not (5 <= d_reading_obj['x_hz'] <= 47):
            alerts['x_hz'] = d_reading_obj['x_hz']
        if 'y_hz' in d_reading_obj and not (5 <= d_reading_obj['y_hz'] <= 31):
            alerts['y_hz'] = d_reading_obj['y_hz']
        if 'z_hz' in d_reading_obj and not (5 <= d_reading_obj['z_hz'] <= 51):
            alerts['z_hz'] = d_reading_obj['z_hz']
        return alerts    
    except Exception as exp:
        raise exp


def get_cmapssdata_mock():
    static_cmapss = {
        "coordinates": {
            "Latitude": "12.9716",
            "Longitude": "77.5946"
        },
        "current": 3,
        "cycle": "10",
        "humidity": 31,
        "id": "1",
        "load": 480,
        "origin": "cmapssdata",
        "power": "55MW",
        "s1": "518.67",
        "s10": "1.30",
        "s11": "47.03",
        "s12": "521.79",
        "s13": "2388.06",
        "s14": "8129.38",
        "s15": "8.4286",
        "s16": "0.03",
        "s17": "393",
        "s18": "2388",
        "s19": "100.00",
        "s2": "641.71",
        "s20": "38.95",
        "s21": "23.4694",
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
    return static_cmapss


if __name__ == "__main__":
    print("Foo")
    # foo = create_mock_data(None)
    foo = get_cmapssdata_mock()
    print(foo)