
import requests
import pprint
import time
import json

url = 'https://api.hh.ru/vacancies'

request_text = 'NAME:'+input('Введите запрос для поиска вакансий:')
key_skills = {}
vacancies_total = 0     #число найденных вакансий
salary_total = 0        #суммарная зарплата вакансий - для расчета средней
NUM_PAGES = 2           #ограничение числа страниц поиска

for page_number in range(NUM_PAGES):

    parameters = {
         'text': request_text,
         'per_page': 10,
         'page': page_number,
         'only_with_salary': True,
         'currency': 'RUR'
    }

    result = requests.get(url, params=parameters).json()
#    print('Страница:', page_number)
#    pprint.pprint(result)
    vacancies = result['items']

    for vacancy in vacancies:
        url_vacancy = vacancy['url']
        result = requests.get(url_vacancy).json()
        salary = result['salary']

        if salary['currency'] == 'RUR':
            print(result['key_skills'])
            print(result['salary'])
            vacancies_total  += 1
            salary_start = 0 if salary['from'] is None else salary['from']
            salary_finish = salary_start if salary['to'] is None else salary['to']
            salary_total  += (salary_start+salary_finish)/2

            skills = result['key_skills']
            for skill in skills:
                item = skill['name']
                if item in key_skills:
                    key_skills[item] += 1
                else:
                    key_skills[item] = 1

            time.sleep(1)

#print(key_skills)

key_skills_sorted = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)

request_result = {}

request_result['vacancies_total'] = vacancies_total
request_result['average_salary'] = round(salary_total/vacancies_total,-3)
request_result['key_skills'] = key_skills_sorted

print('ВСЕГО ВАКАНСИЙ:', vacancies_total)
print('СРЕДНЯЯ ЗАРПЛАТА:', request_result['average_salary'])
print('СПИСОК КЛЮЧЕВЫХ НАВЫКОВ:')
for item in key_skills_sorted:
    print(f'{item[0]} {item[1]}  {round(item[1]/vacancies_total*100)} %' )

request_result_json = json.dumps(request_result)
print(request_result_json)


