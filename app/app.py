from flask import Flask
from flask_restx import Api, Resource
from speech import Speech
from morpheme import Morpheme
<<<<<<< HEAD
=======
import azure.cognitiveservices.speech as speechsdk

# import Mecab
>>>>>>> 88abb58 (merge commit)

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록


api.add_namespace(Speech, '/speech')
api.add_namespace(Morpheme, '/mecab')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)