
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# Импорт необходимых модулей
db = SQLAlchemy() # Создание экземпляра SQLAlchemy для работы с базой данных


class User(db.Model):
    def __init__(self, email: str, firstname: str, lastname: str):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    id = db.Column(db.Integer, primary_key=True) # Поле для хранения идентификатора пользователя
    email = db.Column(db.String(120), unique=True, nullable=False) # Поле для хранения почты пользователя
    firstname = db.Column(db.String(40), nullable=False) # Поле для хранения имени пользователя
    lastname = db.Column(db.String(80), nullable=False) # Поле для хранения фамилии пользователя
    password_hash = db.Column(db.String(128), nullable=False) # Поле для хранения хэша пароля пользователя

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # Метод для установки хэша пароля пользователя

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # Метод для проверки введенного пароля на совпадение с хранимым хешем