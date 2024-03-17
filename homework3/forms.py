
from flask_wtf import FlaskForm # Импорт класса FlaskForm из библиотеки Flask-WTF
from wtforms.fields.simple import StringField, PasswordField, SubmitField # Импорт различных полей для формы
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp # Импорт различных валидаторов

# Класс формы регистрации пользователей
class RegistrationForm(FlaskForm):
    # настройки
    pass_len = 8 # Длина пароля
    regexp = '(?=.*[a-zA-Zа-яА-Я])(?=.*[0-9])[A-Za-zа-яА-Я\\d]{8,}' # Регулярное выражение для пароля
    password_main_message = (f'Пароль должен содержать не менее {pass_len} символов, ' 
                             f'включая хотя бы одну букву и одну цифру.') # Сообщение о требованиях к паролю
    password_secondary_message = f'Подтверждение должно совпадать с паролем.' # Сообщение о совпадении паролей

    # поля
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Email()]) # Поле электронной почты
    firstname = StringField('Имя', validators=[DataRequired(), Length(max=30)]) # Поле имени
    lastname = StringField('Фамилия', validators=[DataRequired(), Length(max=30)]) # Поле фамилии
    password = PasswordField('Пароль',
                             validators=[DataRequired(), Length(min=pass_len),
                                         Regexp(regexp, message=password_main_message)]) # Поле пароля
    confirm_password = PasswordField('Подтверждение пароля',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message=password_secondary_message)]) # Поле подтверждения пароля
    submit = SubmitField('Зарегистрироваться') # Поле кнопки отправки формы

# Класс формы входа пользователя
class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Email()]) # Поле электронной почты
    password = PasswordField('Пароль', validators=[DataRequired()]) # Поле пароля
    submit = SubmitField('Войти') # Поле кнопки отправки формы