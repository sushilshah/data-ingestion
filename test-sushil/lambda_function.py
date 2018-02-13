import ast
import boto3
import json
import decimal

# from dynamodb import DynamoDB

# Helper class to convert a DynamoDB item to JSON.
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             if o % 1 > 0:
#                 return float(o)
#             else:
#                 return int(o)
#         return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    # TODO implement
    data = upsert()
    # dynamo = boto3.client('dynamodb')
    # print('Loading function')
    # # lambda dynamo, x: dynamo.scan(**x)
    # response = dynamo.scan(TableName='device_status',
    #  Select="ALL_ATTRIBUTES",)
   
    # for i in response['Items']:
    #     d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
    #     print(d)
   
    # dynamodb = boto3.resource('dynamodb')
    
    # table = dynamodb.Table('device_status')
    
    # response = table.scan()
    # data = response['Items']
    # print(data)
    
    # client = boto3.client('dynamodb')
    # for item in data:
    #     response = client.put_item(
    #         TableName='vib-mon-sls-device-dev',
    #         Item=json.dumps(item, cls=DecimalEncoder)
    #     )
    #     print(response)
    # table1 = dynamodb.Table('vib-mon-sls-device-dev')
    
    # item = {"updated": 1516814540, "z_mms": 4, "y_mms": 11, "x_mms": 8, "id": "222", "x_hz": 22, "name": "Sensor-300577", "z_hz": 36, "y_hz": 7}
    # for item in data:
    #     response = table1.put_item(Item=item)
        # insert_data_to_mumbai(item)
    #     print(response)
    return data

def insert_data_to_mumbai(item):
    mum_dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    device_table = mum_dynamodb.Table('vib-mon-sls-device-dev')
    response = device_table.put_item(Item=item)
    print(response)
    
def upsert():
    data = {
        "coordinates": {
            "Latitude": "12.9716",
            "Longitude": "77.5946"
        },
        "current": 19,
        "cycle": "4",
        "humidity": 86,
        "id": "OM",
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
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('device_status')
    # response = table.put_item(Item=data)
    table_name = 'device_status'
    key = data['id']
    # response = table.update_item(Key=key,   Item=data)
    response = table.update_item(
        Key={
            'id': key
        },
        ExpressionAttributeNames={
          '#current_val': 'current',
          '#cycle_val' : 'cycle'
        },
        ExpressionAttributeValues={
          ':current': data['current'],
          ':cycle': data['cycle'],
          ':updated': data['updated'],
        },
        UpdateExpression='SET #current_val = :current, '
                         '#cycle_val = :cycle, '
                         'updated = :updated',
        ReturnValues='ALL_NEW',
    )
    
    # response = DynamoDB().update_item(table_name, {'id' : key}, data) #  insert_item(table, device)
    print(response)
    return response 
    
