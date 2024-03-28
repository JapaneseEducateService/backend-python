from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import azure.cognitiveservices.speech as speechsdk
import speechTest
import time
import string

Speech = Namespace('Speech', description='Speech related operations')

@Speech.route('')
class SpeechResource(Resource):
    def get(self):
        result = speechTest.pronunciation_assessment_continuous_from_file()
        return jsonify(result)