def get_TTS(referenceText):
  try:
    from google.cloud import texttospeech
    from dotenv import load_dotenv
    import os
    import time
    import threading

    def delete_file_after_delay(file_path, delay):
      time.sleep(delay)
      if os.path.exists(file_path):
        os.remove(file_path)

    # Google Cloud 서비스 계정 키 파일 경로 설정
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/secrets/google-credentials.json"

    # 클라이언트 인스턴스화
    client = texttospeech.TextToSpeechClient()
    
    # 합성할 텍스트 입력 설정
    synthesis_input = texttospeech.SynthesisInput(text=referenceText)

    # 음성 성별 ("중립")
    voice = texttospeech.VoiceSelectionParams(
      language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # 반환할 오디오 파일 유형 선택
    audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # 선택한 음성 매개변수 및 오디오 파일 유형으로 텍스트 입력에 대해 텍스트-음성 변환 요청 수행
    response = client.synthesize_speech(
      input=synthesis_input, voice=voice, audio_config=audio_config
    )
    audio_file_path = "/app/audio/" + referenceText + ".wav"
    # 응답의 audio_content는 이진 데이터입니다.
    with open(audio_file_path, "wb") as out:
      # 응답을 출력 파일에 씁니다.
      out.write(response.audio_content)
    
    # 지연 후 파일을 삭제하기 위한 타이머 시작
    delay = 30 * 60
    threading.Timer(delay, delete_file_after_delay, args=[audio_file_path, delay]).start()

    return audio_file_path
  except Exception as e:
    return {'error': str(e)} 
