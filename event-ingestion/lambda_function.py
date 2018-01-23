#!/usr/bin/python
import logging
import datetime
from model import Device, Utils
import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    This function inserts content into mysql RDS instance
    """
    # add_device_readings()
    # data_source = [
    # {'field1': 'val1-1', 'field2': 'val1-2'},
    # {'field1': 'val2-1', 'field2': 'val2-2'},
    # # ...
    # ]
    # SensorName	LastCommunicationDate	X_mms	Y_mms	Z_mms	X_hz	Y_hz	Z_hz
    # Sensor-300578	08-08-2017 08:14	20	20.4	16.7	14	12	17
    # Sensor-300578	08-08-2017 08:14	20	20.4	16.7	14	12	17
    # Sensor-300578	08-08-2017 08:14	20	20.4	16.7	14	12	17
    # Sensor-300577	08-08-2017 08:17	25	24.3	10.8	15	11	19

    # Sensor-300578	08-08-2017 08:14	20	20.4	16.7	14	12	17
    
    # logger.info("start setup tables")
    # Utils().setup_tables()
    
    # Utils().load_mock_data()
    # logger.info("setup table and mock data completed")
    try:
        lines = read_csv_s3(event)
        data_source = []
        logger.info("start forming device reading object")
        idx = 0
        for line in lines:
            if idx > 0:
                d_reading_obj = construct_device_reading_data(line)
                if d_reading_obj:
                    data_source.append(d_reading_obj)
            idx += 1
            logger.info("IDX NO %s", idx)
        logger.info("Adding data to the db")
        logger.info(data_source)
        Utils().bulk_insert_device_readings(data_source)
        logger.info("bulk insert successful")
    except Exception as exp:
        logger.exception("Exception occured %s", exp)

    # dt = '08-08-2017 08:14'
    # import datetime
    # datetime_object = datetime.datetime.strptime(dt, '%d-%m-%Y %H:%M')
    # data_source = [
    #     {'device': Device.get_or_create(name='Sensor-300578')[0], 'device_display_time' : datetime_object},
    #     {'device': Device.get_or_create(name='Sensor-300577')[0], 'device_display_time' : datetime_object}
    # ]
    # data_source = [
    #     {'device': Device.get_or_create(name='Sensor-300578') },
    #     {'device': Device.get_or_create(name='Sensor-300577')}
    # ]
    # Utils().bulk_insert_device_readings(data_source)
    # person, created = Device.get_or_create(name='Sensor-300578')
    # print(person, created)
    # print(Device.get_or_create(name='Sensor-300578')[0])

    # foo = DeviceReadings.create(device = Device.get(name='Sensor-300578'))
    # print("device created")
    # print(foo)
    # user = User.create(username='admin', password='test')

    return "Added %d items to RDS MySQL table"


def add_device_readings():
    # huey.courses.add(Course.select().where(Course.name.contains('English')))
    device = Device.get(name='Sensor-300578')
    print(device.id, device.name, device.health)

def construct_device_reading_data(line):
    '''
    Form DeviceReading object
    '''
    logger.info("Construct object for %s", line)
    try:
        tmp = dict()
        tmp['current_amp'] = 10
        tmp['humidity'] = 80
        tmp['power_watt'] = 100
        tmp['temperature'] = 28
        tmp['voltage_volt'] = 440
        tmp['device_packet_time'] = datetime.datetime.now()
        # SensorName	LastCommunicationDate	X_mms	Y_mms	Z_mms	X_hz	Y_hz	Z_hz
        # Sensor-300578	08-08-2017 08:14	20	20.4	16.7	14	12	17
        line = line.split(',')
        tmp['device'] = Device.get_or_create(name=line[0])[0]
        logger.info("after Device get or create")
        dt = line[1]
        datetime_object = datetime.datetime.strptime(dt, '%d-%m-%Y %H:%M')
        #TODO calaulate g value
        # tmp['g_value'] = columns[3]
        tmp['device_display_time'] = datetime_object
        tmp['x_mms'] = line[2]
        tmp['y_mms'] = line[3]
        tmp['z_mms'] = line[4]
        tmp['x_hz'] = line[5]
        tmp['y_hz'] = line[6]
        tmp['z_hz'] = line[7]
        return tmp
    except Exception as exp:
        logger.exception("Not able to construct object for line %s", line)
        logger.exception(exp)
        return None

def read_csv_s3(event):
    '''
    Read file from S3
    '''
    logger.info("Begin file read from S3")
    try:    
        s3 = boto3.client('s3')
        # for bucket in s3.buckets.all():
        #     print(bucket.name)
        bucket = event['bucket'] if 'bucket' in event else 'sim-vib-mon'
        # key = event['key'] if 'key' in event else 'simular-data.csv'
        key = event['key'] if 'key' in event else 'sim-small.csv'
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        lines = [line for line in file_content.split('\r\n')]
        # for line in lines:
        #     print(line.split(','))
        # return 'Hello from Lambda'
        
        logger.info("End file read from S3")
        return lines
    except Exception as exp:
        logger.exception("Exception occured while reading file from s3 %s", exp)
        raise exp


if __name__ == "__main__":
    lambda_handler(None, None)