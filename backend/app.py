from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world!'

@app.route('/get-data')
def get_data():
    ret = {}
    return jsonify(results=ret)
