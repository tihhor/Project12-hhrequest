from flask import Flask, render_template, request
import requests
import pprint
import time
import json
from hhrequest import hh_request

app = Flask(__name__)


@app.route("/")
def main():
    msg = 'Домашнее задание №16'
    return render_template('index.html', message=msg)



@app.route("/index/")
def index():
    msg = 'Домашнее задание №16'
    return render_template('index.html', message=msg)


@app.route('/request/', methods=['GET'])
def request_get():

    return render_template('request.html')

@app.route('/request/', methods=['POST'])
def request_post():
    data = request.form['what']
    request_result = hh_request(data)

    return render_template('results.html', data=request_result)


@app.route('/results/')
def results():
    with open('request_result.json', "r", encoding="utf-8") as f:
        data = json.load(f)
    # print(data)
    return render_template('results.html', data=data)



@app.route('/contact/')
def contacts():

    return render_template('contact.html')





if __name__ == "__main__":
    app.run(debug=True)