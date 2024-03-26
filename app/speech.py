from flask import request
from flask_restx import Resource, Api, Namespace


Speech = Namespace('Speech', description='Speech related operations')

@Speech.route('')
class SpeechResource(Resource):
    def get(self):
        return {"hello": "world!"}