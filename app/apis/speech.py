from flask import request, jsonify
from flask_restx import Resource, Namespace
import core.pronunciation_assessment as pronunciation_assessment
import time


Speech = Namespace('Speech', description='Speech related operations')

@Speech.route('')
class SpeechResource(Resource):
  def post(self):
    audioFile = request.files['audio']
    referenceText = request.form['referenceText']
    
    WaveHeader16K16BitMono = bytes([ 82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0, 125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0 ])

    # def get_chunk(audio_source, chunk_size=1024):
    #   yield WaveHeader16K16BitMono
    #   while True:
    #     time.sleep(chunk_size / 32000) # to simulate human speaking rate
    #     chunk = audio_source.read(chunk_size)
    #     if not chunk:
    #       global uploadFinishTime
    #       uploadFinishTime = time.time()
    #       break
    #     yield chunk

    

    # Validate audio file
    if 'audio' not in request.files:
      return jsonify({'message': 'No audio file part in the request'}), 400
    if audioFile.filename == '':
      return jsonify({'message': 'No selected file'}), 400
    if audioFile and not allowed_file(audioFile.filename):
      return jsonify({'message': 'Invalid audio file'}), 400

    # Validate reference text
    if not referenceText:
      return jsonify({'message': 'No reference text provided'}), 400


    # Validate audio file
    if audioFile and allowed_file(audioFile.filename):
      # Process the audio file here
      result = pronunciation_assessment.get_pronunciation_assessment(audioFile, referenceText)
      return jsonify(result)
    else:
      return jsonify({'message': 'Invalid audio file'})

def allowed_file(filename):
  ALLOWED_EXTENSIONS = {'wav'}  # Add more allowed extensions if needed
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS