from flask_restx import Api
from .morpheme import Morpheme
from .speech import Speech

api = Api(
  title='My Python API',
  version='1.0',
  description='A simple demonstration of a Flask RestPlus powered API',
)

api.add_namespace(Speech, '/speech')
api.add_namespace(Morpheme, '/mecab')