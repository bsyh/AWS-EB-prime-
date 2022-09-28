import boto3, ipaddress, datetime, json
from botocore.exceptions import ClientError
from pprint import pprint

ACCESS_KEY = "YOUR ACCESS_KEY"
SECRET_KEY = "YOUR SECRET_KEY"

def create_session():
    session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    return dynamodb

def ip2int(ip="192.168.0.1"):
    return int(ipaddress.IPv4Address(ip))

def int2ip(ip_int):
    return str(ipaddress.IPv4Address(ip_int))

def time2int(current_date=None):
    if current_date is None:
        current_date = datetime.datetime.now()
    result = \
      current_date.year * 10000000000 + \
      current_date.month * 100000000 + \
      current_date.day * 1000000 + \
      current_date.hour * 10000 + \
      current_date.minute * 100 + \
      current_date.second
    return result

def add_data(dynamodb, table_name, path="demo_data.json"):
    with open(path) as json_file:
        data_list = json.load(json_file)

    table = dynamodb.Table(table_name)

    for data in data_list:
        data["IP"] = int(data[""])
        data["time"] = int(data["time"])
        table.put_item(Item=data)

def get_record(dynamodb, table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    # response = table.scan(
    #     TableName=table_name,
    #     IndexName='time',
    #     AttributesToGet=[
    #         'IP'
    #     ],
    #     Limit=20
    # )

    return response

def create_table(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName = 'IP_history',
            KeySchema = [
                {
                    'AttributeName':'IP',
                    'KeyType':'HASH'
                },
                {
                    'AttributeName':'time',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[

                {
                    'AttributeName': 'IP',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'time',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput = {
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
            }
        )
        return table.table_status
    except Exception as e:
        return e

if __name__ == "__main__":

    dynamodb = create_session()

    # message = create_table(dynamodb)
    # print(message)

    # add_data(dynamodb, "IP_history", path="demo_data.json")

    response = get_record(dynamodb, "IP_history")
    items = response['Items']
    for i in items:
        print(int2ip(int(i['IP'])), end=" ")
        print(i['time'], end=' ')
        print(i['requested_index'])
