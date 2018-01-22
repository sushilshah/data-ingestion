from peewee import *

# database = MySQLDatabase('motovibr', **{'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Tblcountrymaster(BaseModel):
    countrycode = CharField(db_column='CountryCode', null=True)
    countryid = PrimaryKeyField(db_column='CountryID')
    countryname = CharField(db_column='CountryName', null=True)
    countryshortname = CharField(db_column='CountryShortName', null=True)

    class Meta:
        db_table = 'tblcountrymaster'

class Tbldevicemaster(BaseModel):
    devicehealth = IntegerField(db_column='DeviceHealth', null=True)
    deviceid = PrimaryKeyField(db_column='DeviceID')
    devicelocarea = CharField(db_column='DeviceLocArea', null=True)
    deviceloc_x = IntegerField(db_column='DeviceLoc_X')
    deviceloc_y = IntegerField(db_column='DeviceLoc_Y')
    devicename = CharField(db_column='DeviceName', null=True)
    devicestatus = IntegerField(db_column='DeviceStatus', null=True)
    devicetype = CharField(db_column='DeviceType', null=True)

    class Meta:
        db_table = 'tbldevicemaster'

class Tblusermaster(BaseModel):
    commissionstatus = CharField(db_column='CommissionStatus', null=True)
    role = IntegerField(db_column='Role', null=True)
    usermasterid = PrimaryKeyField(db_column='UserMasterID')
    username = CharField(db_column='UserName', null=True)

    class Meta:
        db_table = 'tblusermaster'

class Tbluserdetailstransaction(BaseModel):
    password = CharField(db_column='Password', null=True)
    refreshrate = IntegerField(db_column='RefreshRate', null=True)
    saltvalue = CharField(db_column='SaltValue', null=True)
    updatetime = DateTimeField(db_column='UpdateTime')
    userid = PrimaryKeyField(db_column='UserID')
    usermasterid = ForeignKeyField(db_column='UserMasterID', null=True, rel_model=Tblusermaster, to_field='usermasterid')

    class Meta:
        db_table = 'tbluserdetailstransaction'

class Tblalertconfigtransaction(BaseModel):
    configid = PrimaryKeyField(db_column='ConfigID')
    countryid = ForeignKeyField(db_column='CountryID', null=True, rel_model=Tblcountrymaster, to_field='countryid')
    deviceid = ForeignKeyField(db_column='DeviceID', null=True, rel_model=Tbldevicemaster, to_field='deviceid')
    email = CharField(db_column='Email', null=True)
    mobile = IntegerField(db_column='Mobile', null=True)
    mobilecode = CharField(db_column='MobileCode', null=True)
    name = CharField(db_column='Name', null=True)
    updatetime = DateTimeField(db_column='UpdateTime', null=True)
    userid = ForeignKeyField(db_column='UserID', null=True, rel_model=Tbluserdetailstransaction, to_field='userid')

    class Meta:
        db_table = 'tblalertconfigtransaction'

class Tblalertmaster(BaseModel):
    alertdescription = CharField(db_column='AlertDescription', null=True)
    alertid = PrimaryKeyField(db_column='AlertID')
    alertname = CharField(db_column='AlertName', null=True)
    alerttype = CharField(db_column='AlertType', null=True)
    prioritytype = IntegerField(db_column='PriorityType', null=True)

    class Meta:
        db_table = 'tblalertmaster'

class Tblalerttransaction(BaseModel):
    alertdisplaytime = DateTimeField(db_column='AlertDisplayTime')
    alertid = ForeignKeyField(db_column='AlertID', null=True, rel_model=Tblalertmaster, to_field='alertid')
    alertpacketid = PrimaryKeyField(db_column='AlertPacketID')
    alertpackettime = DateTimeField(db_column='AlertPacketTime')
    current_amp = IntegerField(db_column='Current_Amp', null=True)
    deviceid = ForeignKeyField(db_column='DeviceID', null=True, rel_model=Tbldevicemaster, to_field='deviceid')
    frequency = IntegerField(db_column='Frequency', null=True)
    g_value = FloatField(db_column='G_Value', null=True)
    humidity = IntegerField(db_column='Humidity', null=True)
    power_watt = IntegerField(db_column='Power_Watt', null=True)
    temperature = IntegerField(db_column='Temperature', null=True)
    voltage_volt = IntegerField(db_column='Voltage_Volt', null=True)
    x_value = IntegerField(db_column='X_Value', null=True)
    y_value = IntegerField(db_column='Y_Value', null=True)
    z_value = IntegerField(db_column='Z_Value', null=True)

    class Meta:
        db_table = 'tblalerttransaction'

class Tbldevicetransaction(BaseModel):
    current_amp = IntegerField(db_column='Current_Amp', null=True)
    devicedisplaytime = DateTimeField(db_column='DeviceDisplayTime')
    deviceid = ForeignKeyField(db_column='DeviceID', null=True, rel_model=Tbldevicemaster, to_field='deviceid')
    devicepackettime = DateTimeField(db_column='DevicePacketTime')
    frequency = IntegerField(db_column='Frequency', null=True)
    g_value = FloatField(db_column='G_Value', null=True)
    humidity = IntegerField(db_column='Humidity', null=True)
    packetid = PrimaryKeyField(db_column='PacketID')
    power_watt = IntegerField(db_column='Power_Watt', null=True)
    temperature = IntegerField(db_column='Temperature', null=True)
    voltage_volt = IntegerField(db_column='Voltage_Volt', null=True)
    x_value = IntegerField(db_column='X_Value', null=True)
    y_value = IntegerField(db_column='Y_Value', null=True)
    z_value = IntegerField(db_column='Z_Value', null=True)

    class Meta:
        db_table = 'tbldevicetransaction'