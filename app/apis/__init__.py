from flask_restx import Api
from .morpheme import Morpheme
from .speech import Speech

api = Api(
  title='Tamago Flask API',
  version='1.0',
  description='Tamago Flask API with Swagger UI',
)

api.add_namespace(Speech, '/speech')
api.add_namespace(Morpheme, '/mecab')