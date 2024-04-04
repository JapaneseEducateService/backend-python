from flask import request, jsonify
from flask_restx import Resource, Namespace
import core.pronunciation_assessment as pronunciation_assessment

Speech = Namespace('Speech', description='Speech related operations')

@Speech.route('')
class SpeechResource(Resource):
  def post(self):
    audioFile = request.files['audio']
    referenceText = request.form['referenceText']
    
    # Validate audio file
    if 'audio' not in request.files:
      return jsonify({'message': 'No audio file part in the request'})
    if audioFile.filename == '':
      return jsonify({'message': 'No selected file'})
    if audioFile and not allowed_file(audioFile.filename):
      return jsonify({'message': 'Invalid audio file'})

    # Validate reference text
    if not referenceText:
      return jsonify({'message': 'No reference text provided'})

    # Process the audio file here
    result = pronunciation_assessment.get_pronunciation_assessment(audioFile, referenceText)
    return jsonify(result)
  def get(self):
    return jsonify({'message': 'GET request received'})
    

def allowed_file(filename):
  ALLOWED_EXTENSIONS = {'wav'}  # Add more allowed extensions if needed
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS