# Задание

# Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан cookie-файл с данными пользователя,
# а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными пользователя
# и произведено перенаправление на страницу ввода имени и электронной почты.

from flask import Flask, render_template, make_response, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('authorisation'))

# Страница авторизации
@app.route('/authorisation/', methods=['GET', 'POST'])
def authorisation():
    context = {'title': 'Авторизация'}
    if request.method == 'POST':  # Если данные отправлены методом POST
        username = request.form.get('authorisation_username') # Получить имя пользователя из формы
        email = request.form.get('authorisation_email') # Получить email из формы
        response = make_response(redirect(url_for('index'))) # Создать ответ с перенаправлением на главную страницу
        response.set_cookie('username', username) # Установить cookie 'username'
        response.set_cookie('email', email) # Установить cookie 'email'
        return response
    response = make_response(render_template('authorisation.html', **context)) # Вернуть страницу с формой авторизации
    return response

# Страница выхода (удаление cookie)
@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('index'))) # Создать ответ с перенаправлением на главную
    response.set_cookie('username', '', expires=0) # Удалить cookie 'username'
    response.set_cookie('email', '', expires=0) # Удалить cookie 'email'
    return response


if __name__ == '__main__':
    app.run(debug=True)