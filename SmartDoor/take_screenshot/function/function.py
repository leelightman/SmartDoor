import json
import cv2
import base64
import boto3
from botocore.exceptions import ClientError
import time

def upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def write_to_file(save_path, data):
  with open(save_path, "wb") as f:
    f.write(base64.b64decode(data))
    
def lambda_handler(event, context):
  
    kinesis_client = boto3.client('kinesisvideo')
    response = kinesis_client.get_data_endpoint(
    StreamName='smartdoor-stream',
    #StreamARN='arn:aws:kinesisvideo:us-east-1:838204805079:stream/smartdoor-stream/1572296816863',
    APIName='GET_HLS_STREAMING_SESSION_URL')
    #print(response)
    end_point = response['DataEndpoint']
    #print(end_point)
    
    # # Grab the HLS Stream URL from the endpoint
    kinesis_archive_media_client = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
    url = kinesis_archive_media_client.get_hls_streaming_session_url(
        StreamName='smartdoor-stream',
        PlaybackMode="LIVE"
    )['HLSStreamingSessionURL']
    
    print("url",url)
    print("HLS URL:", url)

    kvs = boto3.client("kinesisvideo")
    response = kvs.list_streams()
    
    print("Stream data:")
    
    for i in range(len(response['StreamInfoList'])):
    
      streaminfo = response['StreamInfoList'][i]
      for key,value in streaminfo.items():
         print(key,':',value)
      streamname = streaminfo['StreamName']
      datapointinfo = kvs.get_data_endpoint(StreamName=streamname, APIName='GET_MEDIA')
      datapoint = datapointinfo['DataEndpoint']
      print(datapoint)
    
    
    # Now try getting video chunks using GetMedia
    
    response = kvs.get_data_endpoint(
        #StreamName=STREAM_NAME,
        StreamARN=hls_stream_ARN,
        APIName='GET_MEDIA'
    )
    
    print("Getting data endpoint...", response)

    endpoint_url_string = response['DataEndpoint']
    
    streaming_client = boto3.client(
    	'kinesis-video-media', 
    	endpoint_url=endpoint_url_string, 
    	#region_name='us-east-1'
    )
    
    kinesis_stream = streaming_client.get_media(
    	StreamARN=hls_stream_ARN,
    	StartSelector={'StartSelectorType': 'EARLIEST'}
    	#StartSelector={'StartSelectorType': 'NOW'}
    
    )
    
    stream_payload = kinesis_stream['Payload']
    
    print("Received stream payload.")
    
    f = open("fragments_"+ str(time.time()) +".mkv", 'w+b')
    f.write(stream_payload.read())
    f.close() 

    print("Saved to a file.")
    return {
      "statusCode": 200,
      'body': json.dumps('Hello from Lambda!')
    }