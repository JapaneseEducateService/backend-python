from flask import Flask
from apis import api
from flask import jsonify
import traceback

app = Flask(__name__)
api.init_app(app)


if __name__ == '__main__':
  app.run(debug=True)

@app.errorhandler(Exception)
def handle_exception(e):
  # "traceback": traceback.format_exc() 개발 단계에서만 사용
  return jsonify({"error": str(e), "traceback": traceback.format_exc()})