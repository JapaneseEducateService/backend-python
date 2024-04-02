def get_pronunciation_assessment(audioFile, referenceText):
  try:
    from dotenv import load_dotenv
    import os
    import requests
    import base64
    import json
    import time

    env_path = '/app/.env'
    load_dotenv(dotenv_path=env_path)

    # 환경 변수 사용
    azure_api_key = os.getenv('AZURE_API_KEY')
    azure_region = os.getenv('AZURE_REGION')

    subscriptionKey = azure_api_key # replace this with your subscription key
    region = azure_region # replace this with the region corresponding to your subscription key, e.g. westus, eastasia

    # a common wave header, with zero audio length
    # since stream data doesn't contain header, but the API requires header to fetch format information, so you need post this header as first chunk for each query
    WaveHeader16K16BitMono = bytes([ 82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0, 125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0 ])

    # a generator which reads audio data chunk by chunk
    # the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
    def get_chunk(audio_source, chunk_size=1024):
      yield WaveHeader16K16BitMono
      while True:
        time.sleep(chunk_size / 32000) # to simulate human speaking rate
        chunk = audio_source.read(chunk_size)
        if not chunk:
          global uploadFinishTime
          uploadFinishTime = time.time()
          break
        yield chunk

    # build pronunciation assessment parameters
    # referenceText_test = "今日は水木です。読みたいテキストをここに入力してください。"
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\"}" % referenceText
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
    getResponseTime = time.time()

    resultJson = json.loads(response.text)

    latency = getResponseTime - uploadFinishTime
    print("Latency = %sms" % int(latency * 1000))
    return { "result" : resultJson , "latency" : int(latency * 1000)}
  except Exception as e:
    return {'error': str(e)}