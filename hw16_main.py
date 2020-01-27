from flask import Flask, render_template, request
import requests
import pprint
import time
import json
from hhrequest import hh_request
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('hh_requests.sqlite', check_same_thread=False)

# Создаем курсор
cursor = conn.cursor()

# cursor.execute('SELECT * from region')
#
# result = cursor.fetchall()
# print(result)

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
    cursor.execute("insert into requests (request_text, vacancies_total, average_salary) "
                   "VALUES (?, ?, ?)", (request_result['request_text'],
                                        request_result['vacancies_total'],
                                        request_result['average_salary']))
    conn.commit()
    cursor.execute('SELECT MAX(id) from requests')
    result = cursor.fetchall()
    curr_id = result[0][0]
    for item in request_result['key_skills']:
        cursor.execute("insert into key_skills (request_id, key_skill_name, key_skill_total) "
                       "VALUES (?, ?, ?)", (curr_id,
                                            item[0],
                                            item[1]))
    conn.commit()


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