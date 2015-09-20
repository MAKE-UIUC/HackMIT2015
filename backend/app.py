from flask import Flask, request, jsonify
import requests
import json
import api

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
