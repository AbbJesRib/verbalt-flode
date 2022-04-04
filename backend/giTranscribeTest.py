import json
import time
import requests
import boto3

transcribe = boto3.client('transcribe')
lambdaclient = boto3.client('lambda')
s3 = boto3.client('s3')
s3_bucket_name = 'pogger'

def lambda_handler(event, context):
    jobName = event['transcriptionName']
    transcription_json = createTranscriptFromFile(jobName)
    # transcript = "Wanted Chief Justice of the Massachusetts Supreme Court in April, the SJC's current leader, Edward Hennessey, reaches the mandatory retirement age of 70 and a successor is expe."
    return {
        'statusCode': 200,
        'body': filtered_result
    }

def createTranscriptFromFile(transcriptName):
    extension = '.wav'
    file_uri = 's3://gitesting/' + transcriptName + extension
    transcribe.start_transcription_job(
        TranscriptionJobName=transcriptName,
        Media={'MediaFileUri': file_uri},
        MediaFormat = extension[1:],
        LanguageCode='en-US')
    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=transcriptName)
        if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(5)
    if result['TranscriptionJob']['TranscriptionJobStatus'] == "COMPLETED":
        filtered_result = lambdaclient.invoke(FunctionName='giAnalyzeTranscribation', Payload=json.dumps({'transcriptName': transcriptName}))
        transcribe.delete_transcription_job(TranscriptionJobName=transcriptName)
        return filtered_result['body']
    transcript = getTranscriptFromName(transcriptName)
    return transcript