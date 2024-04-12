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

    load_dotenv()
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=referenceText)

    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
      language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

  # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
      input=synthesis_input, voice=voice, audio_config=audio_config
    )
    audio_file_path = "/app/audio/" + referenceText + ".wav"
    # The response's audio_content is binary.
    with open(audio_file_path, "wb") as out:
      # Write the response to the output file.
      out.write(response.audio_content)
    
    # Start a timer to delete the file after a delay
    delay = 30 * 60
    threading.Timer(delay, delete_file_after_delay, args=[audio_file_path, delay]).start()

    return audio_file_path
  except Exception as e:
    return {'error': str(e)}  