from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    msg = 'Домашнее задание №16'
    return render_template('index.html', message=msg)


@app.route('/contacts/')
def contacts():
    # где то взяли данные
    developer_name = 'Leo'
    # Контекст name=developer_name - те данные, которые мы передаем из view в шаблон
    # context = {'name': developer_name}
    # Словарь контекста context
    # return render_template('contacts.html', context=context)
    return render_template('contacts.html', name=developer_name, creation_date='16.01.2020')


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


@app.route('/run/', methods=['POST'])
def run_post():
    # Как получть данные формы
    text = request.form['input_text']
    with open('main.txt', 'a') as f:
        f.write(f'{text}\n')
    return render_template('good.html')


if __name__ == "__main__":
    app.run(debug=True)