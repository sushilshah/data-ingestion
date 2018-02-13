import boto3, json
import logging
import time
from random import randint
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    raw_data = get_raw_data()
    # raw_data = get_mock_data()

    item_list = format_to_json(raw_data)
    succ = 0
    fail = 0
    
    _item = {'origin': 'cmapssdata', 'id': '1', 'cycle': '8', 'setting1': '-0.0034', 'setting2': '0.0003', 'setting3': '100.0', 's1': '518.67', 's2': '642.56', 's3': '1582.96', 's4': '1400.97', 's5': '14.62', 's6': '21.61', 's7': '553.85', 's8': '2388.00', 's9': '9040.80', 's10': '1.30', 's11': '47.24', 's12': '522.47', 's13': '2388.03', 's14': '8131.07', 's15': '8.4076', 's16': '0.03', 's17': '391', 's18': '2388', 's19': '100.00', 's20': '38.97', 's21': '23.3106'}
    # response = insert_to_dynamo(_item)
    # batch_write(item_list)
    for item in item_list:
        try:
            item = add_some_mock_vals(item)
            logger.info("inserting item : %s", item)
            logger.info(int(time.time()))
            response = insert_to_dynamo(item)
            succ += 1
            logger.info("**Success $$ : %s", succ)
        except Exception as exp:
            logger.exception(exp)
            fail += 1
            logger.info("**Fail : %s", fail)
    
    logger.info("Success : %s", succ)
    logger.info("Fail : %s", fail)
    
    return {'Hello' : 'World'}

  
  
def batch_write(item_list):
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name='vib-mon-sls-device-dev'
        table = dynamodb.Table(table_name)
        logger.info("Batch ==> %s", item_list)
        with table.batch_writer() as batch:
            for item in item_list:
                batch.put_item(
                    Item=item
                )
    except Exception as exp:
        logger.exception(exp)

    
def insert_to_dynamo(payload) :
    dynamodb = boto3.resource('dynamodb')
    table_name='vib-mon-sls-device-dev'
    # table_name = 'device_status'
    table = dynamodb.Table(table_name)

    response = table.put_item(
        Item=payload
    )
    logger.info("insert_to_dynamo response %s", response)
    return response


def format_to_json(raw_data):
    columns = ['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3',
                     's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14',
                     's15', 's16', 's17', 's18', 's19', 's20', 's21']
    jsons = []                     
    for dataline in raw_data:
        if not dataline:
            continue
        row = dataline.split(' ')
        tmp = dict()
        tmp['origin'] = 'cmapssdata'
        tmp['updated'] = int(time.time())
        for idx, v in enumerate(columns):
            try:
                tmp[v] = row[idx]
            except IndexError as ierr:
                logger.warn("Index not found : [%s]" %(idx))
        jsons.append(tmp)
    return jsons

def get_raw_data():
    file = read_file_from_s3()
    return file

def read_file_from_s3(bucket='cmapssdata', key='sample.txt'):
    # s3://cmapssdata/train_FD001.txt
    # key = 'train_FD001.txt'
    s3 = boto3.client('s3')
    # bucket = event['bucket'] if 'bucket' in event else 'cmapssdata'
    # key = event['key'] if 'key' in event else 'sample.txt'
  
    # key = event['key'] if 'key' in event else 'RUL_FD001.txt'
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')
  
    lines = [line for line in file_content.split('\n')]
  
    return lines

def get_mock_data():
    #data from sample.txt
    return [
            "1 1 -0.0007 -0.0004 100.0 518.67 641.82 1589.70 1400.60 14.62 21.61 554.36 2388.06 9046.19 1.30 47.47 521.66 2388.02 8138.62 8.4195 0.03 392 2388 100.00 39.06 23.4190  ",
            "1 2 0.0019 -0.0003 100.0 518.67 642.15 1591.82 1403.14 14.62 21.61 553.75 2388.04 9044.07 1.30 47.49 522.28 2388.07 8131.49 8.4318 0.03 392 2388 100.00 39.00 23.4236  ",
            "1 3 -0.0043 0.0003 100.0 518.67 642.35 1587.99 1404.20 14.62 21.61 554.26 2388.08 9052.94 1.30 47.27 522.42 2388.03 8133.23 8.4178 0.03 390 2388 100.00 38.95 23.3442  ",
            "1 4 0.0007 0.0000 100.0 518.67 642.35 1582.79 1401.87 14.62 21.61 554.45 2388.11 9049.48 1.30 47.13 522.86 2388.08 8133.83 8.3682 0.03 392 2388 100.00 38.88 23.3739  ",
            "1 5 -0.0019 -0.0002 100.0 518.67 642.37 1582.85 1406.22 14.62 21.61 554.00 2388.06 9055.15 1.30 47.28 522.19 2388.04 8133.80 8.4294 0.03 393 2388 100.00 38.90 23.4044  ",
            "1 6 -0.0043 -0.0001 100.0 518.67 642.10 1584.47 1398.37 14.62 21.61 554.67 2388.02 9049.68 1.30 47.16 521.68 2388.03 8132.85 8.4108 0.03 391 2388 100.00 38.98 23.3669  ",
            "1 7 0.0010 0.0001 100.0 518.67 642.48 1592.32 1397.77 14.62 21.61 554.34 2388.02 9059.13 1.30 47.36 522.32 2388.03 8132.32 8.3974 0.03 392 2388 100.00 39.10 23.3774  ",
            "1 8 -0.0034 0.0003 100.0 518.67 642.56 1582.96 1400.97 14.62 21.61 553.85 2388.00 9040.80 1.30 47.24 522.47 2388.03 8131.07 8.4076 0.03 391 2388 100.00 38.97 23.3106  ",
            "1 9 0.0008 0.0001 100.0 518.67 642.12 1590.98 1394.80 14.62 21.61 553.69 2388.05 9046.46 1.30 47.29 521.79 2388.05 8125.69 8.3728 0.03 392 2388 100.00 39.05 23.4066  ",
            "2 10 -0.0033 0.0001 100.0 518.67 641.71 1591.24 1400.46 14.62 21.61 553.59 2388.05 9051.70 1.30 47.03 521.79 2388.06 8129.38 8.4286 0.03 393 2388 100.00 38.95 23.4694  ",
            ""
    ]

def add_some_mock_vals(item):
    
    mock = item if item else dict()
    '''
    Acceptable values:
    x_mms : 0-18, y_mms : 0-21, z_mms : 0-15, x_hz  : 5-47, y_hz  : 5-31, z_hz  : 5-51'''
    # mock['x_mms'], mock['y_mms'], mock['z_mms'], mock['x_hz'], mock['y_hz'], mock['z_hz'] = \
    # [randint(0,20), randint(0,23), randint(0,20), randint(5,50), randint(5,35), randint(5,53)]
        
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
 

if __name__ == '__main__':
    lambda_handler(None, None)