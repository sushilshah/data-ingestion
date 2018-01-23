import sys
import logging
from peewee import *
# import rds_config
import datetime
import configparser
import os



# rds_host  = rds_config.db_endpoint
# name = rds_config.db_username
# password = rds_config.db_password
# db_name = rds_config.db_name
# port = rds_config.port

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    # db_env = 'LOCAL_DATABASE'
    db_env = 'CLOUD_DATABASE'
    cp = configparser.SafeConfigParser()
    cp.read(os.path.splitext(__file__)[0] + '.ini')
    logging.debug('\n==================================')
    logging.debug('url       : ' + cp.get(db_env, 'db_endpoint'))
    
    rds_host = cp.get(db_env, 'db_endpoint')
    db_username =  cp.get(db_env,'db_username')
    password = cp.get(db_env,'db_password')
    db_name = cp.get(db_env,'db_name')
    port = cp.get(db_env,'port')

# database = MySQLDatabase('motovibr', **{'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': 'root'})
    database = MySQLDatabase(db_name, host=rds_host, port=3306, user=db_username, passwd=password)

    # try:
    #     database.connect()
    #     logger.info("Connected to db")
    # except Exception as e:
    #     logger.error("Unable to connect to the DB")
    #     logger.error(e)

except Exception as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance. %s", e)
    sys.exit()

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Country(BaseModel):
    code = CharField(null=True)
    name = TextField(null=True)
    short_name = CharField(null=True)

    class Meta:
        order_by = ('name',)

class Device(BaseModel):
    health = IntegerField(null=True)
    loc_area = CharField(null=True)
    loc_x = FloatField(null=True)
    loc_y = FloatField(null=True)
    name = TextField(null=True)
    status = IntegerField(null=True)
    devicetype = TextField(null=True)

    class Meta:
         order_by = ('name',)

class User(BaseModel):
    commission_status = TextField(null=True)
    role = IntegerField(null=True)
    user_name = TextField(null=True)
    first_name = TextField( null=True)
    last_name = TextField( null=True)


    class Meta:
         order_by = ('user_name',)        

# class Tbluserdetailstransaction(BaseModel):
#     password = CharField(db_column='Password', null=True)
#     refreshrate = IntegerField(db_column='RefreshRate', null=True)
#     saltvalue = CharField(db_column='SaltValue', null=True)
#     updatetime = DateTimeField(db_column='UpdateTime')
#     userid = PrimaryKeyField(db_column='UserID')
#     usermasterid = ForeignKeyField(db_column='UserMasterID', null=True, rel_model=Tblusermaster, to_field='usermasterid')

#     class Meta:
#         db_table = 'tbluserdetailstransaction'

# class Tblalertconfigtransaction(BaseModel):
#     configid = PrimaryKeyField(db_column='ConfigID')
#     countryid = ForeignKeyField(db_column='CountryID', null=True, rel_model=Tblcountrymaster, to_field='countryid')
#     deviceid = ForeignKeyField(db_column='DeviceID', null=True, rel_model=Tbldevicemaster, to_field='deviceid')
#     email = CharField(db_column='Email', null=True)
#     mobile = IntegerField(db_column='Mobile', null=True)
#     mobilecode = CharField(db_column='MobileCode', null=True)
#     name = CharField(db_column='Name', null=True)
#     updatetime = DateTimeField(db_column='UpdateTime', null=True)
#     userid = ForeignKeyField(db_column='UserID', null=True, rel_model=Tbluserdetailstransaction, to_field='userid')

#     class Meta:
#         db_table = 'tblalertconfigtransaction'

# class Tblalertmaster(BaseModel):
#     alertdescription = CharField(db_column='AlertDescription', null=True)
#     alertid = PrimaryKeyField(db_column='AlertID')
#     alertname = CharField(db_column='AlertName', null=True)
#     alerttype = CharField(db_column='AlertType', null=True)
#     prioritytype = IntegerField(db_column='PriorityType', null=True)

#     class Meta:
#         db_table = 'tblalertmaster'

# class Tblalerttransaction(BaseModel):
#     alertdisplaytime = DateTimeField(db_column='AlertDisplayTime')
#     alertid = ForeignKeyField(db_column='AlertID', null=True, rel_model=Tblalertmaster, to_field='alertid')
#     alertpacketid = PrimaryKeyField(db_column='AlertPacketID')
#     alertpackettime = DateTimeField(db_column='AlertPacketTime')
#     current_amp = IntegerField(db_column='Current_Amp', null=True)
#     deviceid = ForeignKeyField(db_column='DeviceID', null=True, rel_model=Tbldevicemaster, to_field='deviceid')
#     frequency = IntegerField(db_column='Frequency', null=True)
#     g_value = FloatField(db_column='G_Value', null=True)
#     humidity = IntegerField(db_column='Humidity', null=True)
#     power_watt = IntegerField(db_column='Power_Watt', null=True)
#     temperature = IntegerField(db_column='Temperature', null=True)
#     voltage_volt = IntegerField(db_column='Voltage_Volt', null=True)
#     x_value = IntegerField(db_column='X_Value', null=True)
#     y_value = IntegerField(db_column='Y_Value', null=True)
#     z_value = IntegerField(db_column='Z_Value', null=True)

#     class Meta:
#         db_table = 'tblalerttransaction'

class DeviceReadings(BaseModel):
    current_amp = IntegerField(null=True)
    device_display_time = DateTimeField(default=datetime.datetime.now)
    device = ForeignKeyField(Device)
    device_packet_time = DateTimeField(default=datetime.datetime.now)
    g_value = FloatField(null=True)
    humidity = FloatField(null=True)
    power_watt = FloatField(null=True)
    temperature = FloatField(null=True)
    voltage_volt = FloatField(null=True)
    x_hz = FloatField(null=True)
    y_hz = FloatField(null=True)
    z_hz = FloatField(null=True)
    x_mms = FloatField(null=True)
    y_mms = FloatField(null=True)
    z_mms = FloatField(null=True)

    # class Meta:
    #     db_table = 'tbldevicetransaction'
class Test(BaseModel):
    ts = DateTimeField(default=datetime.datetime.now)

class Utils(object):
    
    def bulk_insert_device_readings(self,data_source):
        # Insert rows 100 at a time.
        with database.atomic():
            for idx in range(0, len(data_source), 100):
                DeviceReadings.insert_many(data_source[idx:idx+100]).execute()
                logger.info("Bulk insert of data 100 records from idx %s", idx)

    def setup_tables():
        database.create_tables([Country, Device, User, DeviceReadings])
        logger.info("Tables setup complated")
        # database.create_tables([DeviceReadings])

    def drop_all_tables(self):
        database.drop_table(DeviceReadings)
        database.drop_table(Device)
        database.drop_table(User)
        database.drop_table(Country)
        
    def load_mock_data(self):
        #Add some countries
        country = Country(name = 'India', short_name='IN', code='+91')
        country.save()
        country = Country(name = 'United States', short_name='US', code='+106')
        country.save()
        country = Country(name = 'Australia', short_name='AUS', code='+99')
        country.save()

        #Add some devices
        device = Device(health = 1, loc_area = 'Zone 1', loc_x = 100, loc_y = 100, name = 'Sensor-300578', status = 1, devicetype = 'v-mon-I')
        device.save()
        device = Device(health = 2, loc_area = 'Zone 2', loc_x = 101, loc_y = 101, name = 'Sensor-300577', status = 3, devicetype = 'v-mon-II')
        device.save()
        device = Device(health = 3, loc_area = 'Zone 3', loc_x = 102, loc_y = 102, name = 'Sensor-300575', status = 2, devicetype = 'v-mon-III')
        device.save()
        device = Device(health = 1, loc_area = 'Zone 4', loc_x = 103, loc_y = 103, name = 'Sensor-300579', status = 2, devicetype = 'v-mon-IV')
        device.save()
        device = Device(health = 2, loc_area = 'Zone 5', loc_x = 104, loc_y = 104, name = 'Sensor-195732', status = 3, devicetype = 'v-mon-V')
        device.save()
        
        logger.info("Load Mock Data completed")
        #Add some users


if __name__ == "__main__":
    # Utils().setup_tables()
    test = Test()
    dt = '08-08-2017 08:14'
    print(test.ts)
    datetime_object = datetime.datetime.strptime(dt, '%d-%m-%Y %H:%M')
    print(datetime_object)
    print(type(datetime_object))
