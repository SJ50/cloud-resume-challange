import json
from decimal import Decimal
import boto3

# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VisitorsCountSAM')
# update visitor count    
    try:
        response = table.update_item(
            Key={
                'SiteURL': 'sameerjain.net'
            },
            UpdateExpression="set visitorscount = visitorscount + :val",
            ExpressionAttributeValues={
                ':val': Decimal(1)
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        print("ClientError occured")
        print("Adding record")
        response = table.put_item(
            Item={
                'SiteURL': 'sameerjain.net',
                'visitorscount': 1
            }
        )
    else:
 #   return visitcount
 # https://hometechtime.com/how-to-return-multiple-attributes-from-dynomodb-via-a-lambda-function-and-api-gateway/
 # class DecimalEncoder to Resolve “errorMessage”: “Object of type Decimal is not JSON serializable”

        class DecimalEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Decimal):
                    return int(obj)
                return json.JSONEncoder.default(self, obj)
 
 # headers to allow CORS

        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps(response["Attributes"]["visitorscount"],cls=DecimalEncoder)
        }
