from flask import Flask, render_template, request

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
    data = request.data
    print(data)

    return render_template('request.html')


@app.route('/contact/')
def contacts():
    # где то взяли данные
    developer_name = 'Leo'
    # Контекст name=developer_name - те данные, которые мы передаем из view в шаблон
    # context = {'name': developer_name}
    # Словарь контекста context
    # return render_template('contacts.html', context=context)
    return render_template('contact.html', name=developer_name, creation_date='16.01.2020')


@app.route('/results/')
def results():
    data = ['python', 'js', 'java', 'sql', 'lua']
    # data = []
    return render_template('results.html', data=data)


@app.route('/run/', methods=['GET'])
def run_get():
    with open('main.txt', 'r') as f:
        text = f.read()
    return render_template('form.html', text=text)
    # with open('main.txt', 'a') as f:
    #     f.write('hello')


@app.route('/request/', methods=['POST'])
def req_post():
    # Как получть данные формы
    data = request.data
    print(data)
    # with open('main.txt', 'a') as f:
    #     f.write(f'{text}\n')
    return render_template('request.html')


if __name__ == "__main__":
    app.run(debug=True)