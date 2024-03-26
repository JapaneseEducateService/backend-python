from flask import request
from flask_restx import Resource, Api, Namespace


Morpheme = Namespace('Morpheme', description='Speech related operations')

@Morpheme.route('')
class MorphemeResource(Resource):
    def get(self):
        return {"hello": "world!"}