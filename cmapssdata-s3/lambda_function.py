import boto3

def lambda_handler(event, context):
    # raw_data = get_raw_data()
    raw_data = get_mock_data()
    # print(raw_data)

    foo = format_to_json(raw_data)
    print(foo)
    return raw_data

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
        for idx, v in enumerate(columns):
            try:
                print(row[idx], idx, v)
                tmp[v] = row[idx]
            except IndexError as ierr:
                print("Index not found : [%s]" %(idx))
                print(ierr)
            print(idx, v)
        jsons.append(tmp)
    return jsons

def get_raw_data():
    file = read_file_from_s3()
    return file

def read_file_from_s3(bucket='cmapssdata', key='sample.txt'):
    # s3://cmapssdata/train_FD001.txt
    s3 = boto3.client('s3')
    # for bucket in s3.buckets.all():
    #     print(bucket.name)
    # bucket = event['bucket'] if 'bucket' in event else 'cmapssdata'
    # key = event['key'] if 'key' in event else 'sample.txt'
  
    # key = event['key'] if 'key' in event else 'RUL_FD001.txt'
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')
  
    lines = [line for line in file_content.split('\n')]
    for line in lines:
        print(line.split(','))
    # return 'Hello from Lambda'
  
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
            "1 10 -0.0033 0.0001 100.0 518.67 641.71 1591.24 1400.46 14.62 21.61 553.59 2388.05 9051.70 1.30 47.03 521.79 2388.06 8129.38 8.4286 0.03 393 2388 100.00 38.95 23.4694  ",
            ""
    ]

if __name__ == '__main__':
    lambda_handler(None, None)