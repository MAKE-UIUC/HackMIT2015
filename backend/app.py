from flask import Flask, request, jsonify
import requests
import json
import api
import nasdaq

app = Flask(__name__)

cache = {}

@app.route('/')
def index():
    return 'Hello world!'

@app.route('/get-data/<name>')
def get_data(name=None):
    if name in cache:
        return cache[name]

    ret = api.extractArticleText(name)
    cache[name] = jsonify(results=ret)
    return cache[name]

@app.route('/get-nasdaq/<name>')
def get_nasdaq(name=None):
    ret = nasdaq.nasdaq(name)
    return jsonify(results=ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
