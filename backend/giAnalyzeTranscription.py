import json
import time
import requests
import boto3

transcribe = boto3.client('transcribe')
lambdaclient = boto3.client('lambda')
s3 = boto3.client('s3')
s3_bucket_name = 'pogger'

def lambda_handler(event, context):
    jobName = event['transcriptName']
    s3.download_file(s3_bucket_name, 'animals.txt', '/tmp/'+'animals.txt')
    animals_wordlist = open('/tmp/animals.txt').read().split('\n') 
    transcript_with_timestamps = getTranscriptFromName(jobName)
    transcript_filtered = filterTranscript(transcript_with_timestamps)
    corrects, erroneous, transcript_with_timestamps_and_assessment = assessWords(transcript_filtered, animals_wordlist)
    return {
        'statusCode': 200,
        'body': json.dumps([corrects, erroneous, transcript_with_timestamps_and_assessment])
    }

def getTranscriptFromName(transcriptName):
    # try:
        response = transcribe.get_transcription_job(TranscriptionJobName=transcriptName)
        transcript = response['TranscriptionJob']['Transcript']
        job_transcript = requests.get(
            transcript['TranscriptFileUri']).json()
        full_transcript = job_transcript['results']['transcripts'][0]['transcript']
        def fetchStartTime(item):
            if 'start_time' in item.keys():
                return item['start_time']
        timestamps = [fetchStartTime(item) for item in job_transcript['results']['items']]
        transcript_with_timestamps = list(zip(full_transcript, timestamps))
        return (full_transcript, timestamps)
    # except:
    #     return 'Transcription not found or not ready'

def filterTranscript(transcript_with_timestamps):
    transcript, timestamps = transcript_with_timestamps
    timestamps = list(filter(None, timestamps))
    def removePunctuation(transcript):
        s = ''
        punctuations = ['.', ',', ':', ';']
        for char in transcript:
            if not char in punctuations:
                s += char
        return s
    def capitalization(word):
        try:
            word = word[0].upper() + word[1:]
        except:
            word = word.upper() # if word is one letter long
        return word
    transcript = removePunctuation(transcript)
    words = transcript.split(' ')
    words_formatted = []
    for word in words:
        words_formatted.append(capitalization(word))
    filtered_transcript_with_timestamps = list(zip(words_formatted, timestamps))
    return filtered_transcript_with_timestamps

def assessWords(filtered_transcript_with_timestamps, wordlist):
    transcript, timestamps = list(zip(*filtered_transcript_with_timestamps))
    corrects = 0
    erroneous = 0
    record = []
    for word in transcript:
        isIn = int(word in wordlist or word[:-1] in wordlist) # if candidate says 'Cats' instead of 'Cat', it should still count
        corrects += isIn
        erroneous += 1 - isIn
        record.append(isIn)
    transcript_with_timestamps_and_assessment = list(zip(transcript, record, timestamps))
    return (corrects, erroneous, transcript_with_timestamps_and_assessment)