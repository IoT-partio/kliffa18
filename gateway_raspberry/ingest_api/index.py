from flask import Flask, jsonify
app = Flask(__name__)


temperatures = [
  20, 30.2, 21.2
]

@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route("/temperatures")
def get_temperatures():
    return jsonify(temperatures)

@app.route("/temperatures", methods=['POST'])
def post_temperature():
    temperatures.append(request.get_json())
    return '',204
    