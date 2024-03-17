# Задание

# Создать форму для регистрации пользователей на сайте. 
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". 
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

# Подключение необходимых модулей
import os

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import CSRFProtect

from forms import RegistrationForm, LoginForm # Импорт классов форм регистрации и входа
from models import db, User # Импорт моделей базы данных

# Создание экземпляра Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'development_secret_key' # Установка секретного ключа для безопасности
csrf = CSRFProtect(app)
DB_NAME = 'homework3.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Установка пути к базе данных
db.init_app(app) # Инициализация базы данных с помощью Flask приложения

# Команды для управления базой данных через CLI
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("clear-db")
def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Очищена таблица: {table}')
        db.session.execute(table.delete())
    db.session.commit()



# Установка маршрутов
@app.route('/')
def index():
    return redirect(url_for('login'))

# Регистрация пользователей
@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            message = f'Пользователь с таким email уже существует.'
            flash(message, 'error')
            return redirect(url_for('registration'))

        user = User(firstname=firstname, lastname=lastname, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        message = f'Пользователь {email} успешно зарегистрирован.'
        flash(message, 'success')

    return render_template('registration.html', form=form)

# Вход пользователя
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            message = f'You are welcome, {email}!'
            flash(message, 'success')
        else:
            message = f'Пользователь не найден.'
            flash(message, 'error')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

# Запуск приложения
if __name__ == '__main__':

    if DB_NAME not in os.listdir(os.path.abspath('instance/')):
        init_db() # Инициализация базы данных, если она не существует
    app.run(debug=True) # Запуск сервера Flask в режиме отладки