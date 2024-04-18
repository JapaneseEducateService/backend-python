from flask import Flask
from apis import api
from flask import jsonify

app = Flask(__name__)
api.init_app(app)

if __name__ == '__main__':
  app.run(debug=True)

@app.errorhandler(Exception)
def handle_exception(e):
  print(str(e))
  return jsonify({"error": str(e)})