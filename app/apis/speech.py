from flask import request, jsonify
from flask_restx import Resource, Namespace
import core.pronunciation_assessment as pronunciation_assessment
import core.pitch_comparison as pitch_comparison
import core.google_text_to_speech as google_text_to_speech
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
    
    
    pronunciationAssessmentResult = pronunciation_assessment.get_pronunciation_assessment(audioFile, referenceText)
    audioFile.seek(0)
    pitchComparisonResult = pitch_comparison.get_pitch_comparison(audioFile, referenceText)
    
    

    return jsonify({'pitchComparisonResult': pitchComparisonResult,
                     'pronunciationAssessmentResult': pronunciationAssessmentResult})

# This route is Test API
# @Speech.route('/compare-pitch')
# class PitchComparisonResource(Resource):
#   def post(self):
#     audioFile = request.files['audio']
#     referenceText = request.form['referenceText']
    
#     # Validate audio file
#     if 'audio' not in request.files:
#       return jsonify({'message': 'No audio file part in the request'})
#     if audioFile.filename == '':
#       return jsonify({'message': 'No selected file'})
#     if audioFile and not allowed_file(audioFile.filename):
#       return jsonify({'message': 'Invalid audio file'})
#     # Validate reference text
#     if not referenceText:
#       return jsonify({'message': 'No reference text provided'})
    
#     # Process the audio files here to compare pitch
#     response = pitch_comparison.get_pitch_similarity(audioFile, referenceText)
#     return jsonify(response)

@Speech.route('/tts')
class GoogleTTS(Resource):
  def get(self):
    referenceText = request.form['referenceText']
    if not referenceText:
      return jsonify({'message': 'No reference text provided'})
    
    response = google_text_to_speech.get_TTS(referenceText)
    return jsonify(response)
  
def allowed_file(filename):
  ALLOWED_EXTENSIONS = {'wav'}  # Add more allowed extensions if needed
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS