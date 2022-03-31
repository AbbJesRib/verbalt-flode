import json
import time
import requests
import boto3

transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    # TODO implement
    jobName = event['transcriptionName']
    transcript_with_timestamps = createTranscriptFromFile(jobName)
    # transcript = "Wanted Chief Justice of the Massachusetts Supreme Court in April, the SJC's current leader, Edward Hennessey, reaches the mandatory retirement age of 70 and a successor is expe."
    transcript_filtered = filterTranscript(transcript_with_timestamps)
    return {
        'statusCode': 200,
        'body': json.dumps(transcript_filtered)
    }

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
    filtered_transcript_with_timestamps = zip(words_formatted, timestamps)
    return filtered_transcript_with_timestamps

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
        transcript = getTranscriptFromName(transcriptName)
        transcribe.delete_transcription_job(TranscriptionJobName=transcriptName)
        return transcript
    transcript = getTranscriptFromName(transcriptName)
    return transcript

def getTranscriptFromName(transcriptName):
    try:
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
    except:
        return 'Transcription not found or not ready'