# Ипорт объекта приложения Flask с именем app из модуля main.
from main import app

if __name__ == "__main__": # Проверка, что скрипт запускается непосредственно, а не импортируется в другой скрипт.
    app.run(debug=True) # Запуск встроенного сервера Flask для обслуживания веб-приложения