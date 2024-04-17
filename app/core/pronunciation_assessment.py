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

    # a common wave header, with zero audio length
    # since stream data doesn't contain header, but the API requires header to fetch format information, so you need post this header as first chunk for each query
    WaveHeader16K16BitMono = bytes([ 82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0, 125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0 ])

    # build pronunciation assessment parameters
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"Granularity\":\"Word\" ,\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\"}" % referenceText
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ja-jp" % region
    headers = { 'Accept': 'application/json;text/xml',
                'Connection': 'Keep-Alive',
                'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
                'Ocp-Apim-Subscription-Key': subscriptionKey,
                'Pronunciation-Assessment': pronAssessmentParams,
                'Transfer-Encoding': 'chunked',
                'Expect': '100-continue' }


    # send request with chunked data
    response = requests.post(url=url, data=audioFile, headers=headers)

    resultJson = json.loads(response.text)

    accuracyScore =  resultJson.get('NBest')[0].get('AccuracyScore', 'Not Available')
    fluencyScore = resultJson.get('NBest')[0].get('FluencyScore', 'Not Available')
    completenessScore = resultJson.get('NBest')[0].get('CompletenessScore', 'Not Available')
    pronScore = resultJson.get('NBest')[0].get('PronScore', 'Not Available')
    words = resultJson.get('NBest')[0].get('Words', 'Not Available')
    displayText = resultJson.get('NBest')[0].get('Display', 'Not Available')

    return {
             "AccuracyScore": accuracyScore,
             "FluencyScore": fluencyScore,
             "CompletenessScore": completenessScore,
             "PronScore": pronScore,
             "Words": words ,
             "Display": displayText}
  
  except Exception as e:
    return {'error': str(e)}
  