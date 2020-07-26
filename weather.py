from flask import Flask, render_template, request
# import json to load JSON data to a python dictionary
import json

# urllib.request to make a request to api
import urllib.request

app = Flask(__name__)

@app.route('/', methods =['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city']