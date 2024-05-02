def get_pronunciation_assessment(audioFile, referenceText):
  try:
    from dotenv import load_dotenv
    import os
    import requests
    import base64
    import json

    env_path = '/app/.env'
    load_dotenv(dotenv_path=env_path)

    subscriptionKey = os.getenv('AZURE_API_KEY')
    region = os.getenv('AZURE_REGION')

    # build pronunciation assessment parameters
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"Granularity\":\"Phoneme\" ,\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\"}" % referenceText
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = f"https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ja-jp" % region
    headers = { 'Accept': 'application/json;text/xml',
                'Connection': 'Keep-Alive',
                'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
                'Ocp-Apim-Subscription-Key': subscriptionKey,
                'Pronunciation-Assessment': pronAssessmentParams,
                'Expect': '100-continue' }


    audioData = audioFile.read()
    response = requests.post(url=url, data=audioData, headers=headers)

    resultJson = json.loads(response.text)

    accuracyScore =  resultJson.get('NBest')[0].get('AccuracyScore', 'Not Available')
    fluencyScore = resultJson.get('NBest')[0].get('FluencyScore', 'Not Available')
    completenessScore = resultJson.get('NBest')[0].get('CompletenessScore', 'Not Available')
    pronScore = resultJson.get('NBest')[0].get('PronScore', 'Not Available')
    words = resultJson.get('NBest')[0].get('Words', 'Not Available')
    displayText = resultJson.get('NBest')[0].get('Display', 'Not Available')

    return resultJson
    return {
             "AccuracyScore": accuracyScore,
             "FluencyScore": fluencyScore,
             "CompletenessScore": completenessScore,
             "PronScore": pronScore,
             "Words": words ,
             "Display": displayText}
  
  except Exception as e:
    return {'error': str(e)}
  