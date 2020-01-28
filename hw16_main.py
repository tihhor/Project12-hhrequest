from flask import Flask, render_template, request
import requests
import pprint
import time
import json
from hhrequest import hh_request
import sqlite3
import datetime


# Подключение к базе данных
conn = sqlite3.connect('hh_requests.sqlite', check_same_thread=False)

# Создаем курсор
cursor = conn.cursor()

# cursor.execute('SELECT * from region')
#
# result = cursor.fetchall()
# print(result)

app = Flask(__name__)

def req_result_select(previous_request_id):
    request_result = {}      #записвываем результаты в словарь
    cursor.execute('SELECT request_text, vacancies_total, average_salary, request_time  '
                   'from requests where id=?', (previous_request_id,))
    select_result = cursor.fetchone()
    print(select_result)
    request_result['request_text'] = select_result[0]
    request_result['vacancies_total'] = select_result[1]
    request_result['average_salary'] = select_result[2]
    request_result['request_time'] = select_result[3]


    cursor.execute('SELECT key_skill_name, key_skill_total '
                   'from key_skills where request_id=?', (previous_request_id,))
    select_result = cursor.fetchall()
    request_result['key_skills'] = select_result

    return request_result

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
    req_data = request.form['what']
    # проверяем, был ли такой запрос ранее
    cursor.execute('SELECT id from requests where request_text=?', (req_data,))
    previous_request_id =  cursor.fetchone()
    # print('Предудущий запрос id:', previous_request_id)
    if previous_request_id:   #если раньше был такой запрос, получаем данные из базы данных
        request_result = req_result_select(previous_request_id[0])
    else:   # если такого запроса не было, получаем данные с headhunter
        request_result = hh_request(req_data)

        now = datetime.datetime.now()
        request_result['request_time'] = now.strftime("%d-%m-%Y %H:%M")
        cursor.execute("insert into requests (request_text, vacancies_total, average_salary, request_time) "
                       "VALUES (?, ?, ?, ?)", (request_result['request_text'],
                                            request_result['vacancies_total'],
                                            request_result['average_salary'],
                                            request_result['request_time']))
        #conn.commit()
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
    # выводим данные последней записи в базе данных
    cursor.execute('SELECT MAX(id) from requests')
    previous_request_id = cursor.fetchone()
    print(previous_request_id)
    request_result = req_result_select(previous_request_id[0])

    # with open('request_result.json', "r", encoding="utf-8") as f:
    #     data = json.load(f)
    # print(data)
    return render_template('results.html', data=request_result)



@app.route('/contact/')
def contacts():

    return render_template('contact.html')





if __name__ == "__main__":
    app.run(debug=True)