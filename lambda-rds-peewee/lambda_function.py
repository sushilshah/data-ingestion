#!/usr/bin/python
import sys
import logging
# import rds_config
# import pymysql
# import peewee as pw
from model import Device, DeviceReadings, Utils
# rds_host  = rds_config.db_endpoint
# name = rds_config.db_username
# password = rds_config.db_password
# db_name = rds_config.db_name
# port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# try:

#     myDB = pw.MySQLDatabase(db_name, host=rds_host, port=3306, user=name, passwd=password)


#     # conn = pymysql.connect(rds_host, user=name,
#                            # passwd=password, db=db_name, connect_timeout=5)
# except:
#     logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
#     sys.exit()

# logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def lambda_handler(event, context):
    add_device_readings()
    """
    This function inserts content into mysql RDS instance
    """
    # class MySQLModel(pw.Model):
    #     '''
    #     base model that will use our MySQL database
    #     '''
    #     class Meta:
    #         database = myDB

    # class User(MySQLModel):
    #     username = pw.CharField()
    #     # etc, etc


    # # when you're ready to start querying, remember to connect
    # try:
    #     myDB.connect()
    #     logger.info("Connected to db")
    # except Exception as e:
    #     logger.error("Unable to connect to the DB")
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
    dt = '08-08-2017 08:14'
    import datetime
    datetime_object = datetime.datetime.strptime(dt, '%d-%m-%Y %H:%M')
    data_source = [
        {'device': Device.get_or_create(name='Sensor-300578')[0], 'device_display_time' : datetime_object},
        {'device': Device.get_or_create(name='Sensor-300577')[0], 'device_display_time' : datetime_object}
    ]
    # data_source = [
    #     {'device': Device.get_or_create(name='Sensor-300578') },
    #     {'device': Device.get_or_create(name='Sensor-300577')}
    # ]
    Utils().bulk_insert_device_readings(data_source)
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


# def bulk_insert(data_source):
#     # Insert rows 100 at a time.
#     with db.atomic():
#         for idx in range(0, len(data_source), 100):
#             DeviceReadings.insert_many(data_source[idx:idx+100]).execute()

if __name__ == "__main__":
    lambda_handler(None, None)