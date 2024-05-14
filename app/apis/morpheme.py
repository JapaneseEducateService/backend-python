from flask import request,jsonify
from flask_restx import Resource, Api, Namespace
import MeCab
import jaconv
from flask_restx import fields
Morpheme = Namespace('Morpheme', description='형태소 분석 서비스 API')

MorphemePostResponseModel = Morpheme.model('Model', {	  
  'source' : fields.List(description="형태소 분석한 텍스트", required=True, example="学校、先生、生徒、勉強、日本語、勉強"),
  'gana': fields.List(description="히라가나", required=True, example="がっこう、せんせい、せいと、べんきょう、にほんご、べんきょう"),
  'speak': fields.List(description="발음", required=True, example="ガッコウ、センセイ、セイト、ベンキョウ、ニホンゴ、ベンキョウ")
})


@Morpheme.route('')
class MorphemeResource(Resource):
	
	@Morpheme.doc(responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'})
	@Morpheme.response(code=200, description='Success', model=MorphemePostResponseModel)
	@Morpheme.param(name='texts', description='형태소 분석할 텍스트', _in='body', required=True, type='string', example="['学校、先生、生徒、勉強、日本語、勉強']")
	def post(self):
		# Mecab 객체 초기화
		mecab = MeCab.Tagger('')
		# Laravel에서 받아온 데이터 추출
		texts = request.json['texts']
		result = []
		# 분석할 텍스트
		for text in texts:
			parsed = [[chunk.split('\t')[0], tuple(chunk.split('\t')[1].split(','))] for chunk in mecab.parse(text).splitlines()[:-1]]
			result.append(parsed)
		compare_result = compare_to_morpheme(result)
		source = compare_result['source']
		gana = compare_result['gana']
		speak = compare_result['speak']
		for i in range(len(gana)):
			gana[i] = convert_to_hiragana(gana[i])
			speak[i] = convert_to_hiragana(speak[i])
		return jsonify({'source': source,'gana': gana, 'speak': speak})
  
# mecab 초기 결과에서動詞、形容詞、名詞만 추출
def compare_to_morpheme(parsed):
	# p[0][1][0] = 품사 , p[0][1][6] = 원형, p[0][1][7] = 히라가나, p[0][1][8] = 발음
	source, gana, speak = [], [], []
	for p in parsed:
		if len(p) > 0 and len(p[0]) > 1 and len(p[0][1]) > 8:
			if p[0][1][0] == '名詞' or p[0][1][0] == '動詞' or p[0][1][0] == '形容詞':
				source.append(p[0][1][6])
				gana.append(p[0][1][7])
				speak.append(p[0][1][8])
	return {'source': source, 'gana': gana, 'speak': speak}

# 품사 비교 후 가타카나로 나온 결과들을 -> 히라가나로 변환
def convert_to_hiragana(text):
  # 가타카나 -> 히라가나 변환
  hiragana = jaconv.kata2hira(text)
  return hiragana

