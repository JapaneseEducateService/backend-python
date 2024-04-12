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

    # a generator which reads audio data chunk by chunk
    # the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
    def get_chunk(audio_source, chunk_size=1024):
      yield WaveHeader16K16BitMono
      while True:
        chunk = audio_source.read(chunk_size)
        if not chunk:
          break
        yield chunk

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
    response = requests.post(url=url, data=get_chunk(audioFile), headers=headers)

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
  
# def get_pronunciation_assessment(audioFile, referenceText):
#   try:
#     from dotenv import load_dotenv
#     import os
#     import requests
#     import base64
#     import json
#     import time

#     # 환경 변수 로딩
#     env_path = '/app/.env'
#     load_dotenv(dotenv_path=env_path)

#     # API 키와 지역 정보 로딩
#     subscriptionKey = os.getenv('AZURE_API_KEY')
#     region = os.getenv('AZURE_REGION')

#     # 발음 평가 매개변수 구성
#     pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"Granularity\":\"Word\" ,\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\"}" % referenceText
#     pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
#     pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

#     # 요청 URL 및 헤더 구성
#     url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ja-jp"
#     headers = {
#       'Accept': 'application/json;text/xml',
#       'Connection': 'Keep-Alive',
#       'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
#       'Ocp-Apim-Subscription-Key': subscriptionKey,
#       'Pronunciation-Assessment': pronAssessmentParams,
#     }

#     # 오디오 파일 전체를 읽고 요청 보내기
#     audio_data = audioFile.read()
#     response = requests.post(url=url, data=audio_data, headers=headers)
#     getResponseTime = time.time()

#     # 결과 처리
#     resultJson = json.loads(response.text)
#     latency = getResponseTime - time.time()
#     print(f"Latency = {int(latency * 1000)}ms")
    
#     fluencyScore = resultJson.get('NBest')[0].get('FluencyScore', 'Not Available')
#     prosodyScore = resultJson.get('NBest')[0].get('ProsodyScore', 'Not Available')
#     pronScore = resultJson.get('NBest')[0].get('PronScore', 'Not Available')
#     AccuracyScore =  resultJson.get('NBest')[0].get('AccuracyScore', 'Not Available')
#     CompletenessScore = resultJson.get('NBest')[0].get('CompletenessScore', 'Not Available')
    
    
#     return {"result": resultJson,
#             "latency": int(latency * 1000),
#             "AccuracyScore": AccuracyScore,
#             "FluencyScore": fluencyScore,
#             "CompletenessScore": CompletenessScore,
#             "ProsodyScore": prosodyScore,
#             "PronScore": pronScore,
#             "latency": int(latency * 1000)}
#   except Exception as e:
#     return {'error': str(e)}