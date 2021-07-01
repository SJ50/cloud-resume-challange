import json
from decimal import Decimal
import boto3

# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
 
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VisitorsCountSAM')
    # reqest country
    country = event['headers']['CloudFront-Viewer-Country']
    # request ip
    ip = event['requestContext']['identity']['sourceIp']
    # request time
    lastvisittime = event['requestContext']['requestTime']
    visitorscount = 1
    # request user agent
    #userAgent= event['requestContext']['identity']['userAgent']

# update visitor visitorscount    
    def updatecount(country, ip, visitorscount, lastvisittime):
        try:
            response = table.update_item(
                Key={
                    'Country': country,
                    'IP': ip,
                },
                UpdateExpression="set VisitorsCount = VisitorsCount + :val",
                ExpressionAttributeValues={
                    ':val': Decimal(visitorscount)
                },
                ReturnValues="UPDATED_NEW"
            )
            return response["Attributes"]["VisitorsCount"]
        except Exception as e:
            response = table.put_item(
                Item={
                    'Country': country,
                    'IP': ip,
                    'LastVisitTime': lastvisittime,
                    'VisitorsCount': visitorscount
                }
            )
            return visitorscount
            
    updatecount(country, ip, visitorscount, lastvisittime)
    response = updatecount("ALL", "0.0.0.0", visitorscount, lastvisittime)
    
 # https://hometechtime.com/how-to-return-multiple-attributes-from-dynomodb-via-a-lambda-function-and-api-gateway/
 # class DecimalEncoder to Resolve “errorMessage”: “Object of type Decimal is not JSON serializable”
 #       class DecimalEncoder(json.JSONEncoder):
 #           def default(self, obj):
 #               if isinstance(obj, Decimal):
 #                   return int(obj)
 #               return json.JSONEncoder.default(self, obj)
 
 # headers to allow CORS
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        },
        'body': json.dumps(int(response))
    }
