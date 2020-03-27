from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import datetime

dynamodb = boto3.resource("dynamodb", region_name="us-east-1", endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

table = dynamodb.Table('visitors')
count =0
with open("test.json") as json_file:
    data = json.load(json_file)
    faces = data["faces"]
    #print(restaurants)
    count=0
    for face in faces:
        faceId = face['faceId']
        name = face['name']
        phoneNumber = face['phoneNumber']
        photos = face['photos']
        objectKey = photos[0]['objectKey']
        bucket = photos[0]['bucket']
        createdTimestamp = photos[0]['createdTimestamp']
        
        table.put_item(
           Item={
               'faceId': faceId,
               'name': name,
               'phoneNumber': phoneNumber,
               'photsObjectKey':objectKey,
               'photosBucket':bucket,
               'photosCreatedTimestamp': createdTimestamp,
            }
        )
        
        count+=1
    print(count)
# snippet-end:[dynamodb.python.codeexample.MoviesLoadData]