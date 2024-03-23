# Импорт модулей os и sys для работы с операционной системой и системными параметрами соответственно.
import os
import sys

from homework6.shop import router_items

sys.path.append(rf'{os.path.abspath('shop/')}') # Добавление пути к каталогу "shop" в список путей, где Python ищет модули для импорта.
from fastapi import FastAPI # Импорт класса FastAPI из модуля fastapi для создания экземпляра веб-приложения.
from uvicorn import run as uvi_run # Импорт функции run из модуля uvicorn, которая используется для запуска FastAPI приложения.
from fastapi.responses import RedirectResponse # Импорт класса RedirectResponse для выполнения перенаправления веб-страницы.

from shop import router_users, router_orders # Импорт модулей с роутерами для пользователей, товаров и заказов.
from shop.populate_db import populate # Импорт функции populate из файла populate_db для заполнения базы данных сгенерированными данными.

app = FastAPI() # Создание экземпляря FastAPI под именем app.


@app.get('/populate_db/', tags=['Наполнение БД сгенерированными данными'], response_model=dict) # Обработчик маршрута для заполнения базы данных.
async def populate_db():
    await populate()
    return {'message': 'Успешное заполнение БД'}

# Регистрация маршрутов для пользователей, товаров и заказов.
app.include_router(router_users.router)
app.include_router(router_items.router)
app.include_router(router_orders.router)


@app.get('/', tags=['Redirect to Swagger UI'], response_class=RedirectResponse) # Обработчик маршрута для перенаправления на Swagger UI.
async def redirect_index():
    return "http://127.0.0.1:8000/docs"

# Этот блок будет выполнен только в случае, если данный скрипт запускается как основной скрипт.
if __name__ == "__main__":
    uvi_run("main:app", host="127.0.0.1", port=8000, reload=True) # Запуск приложения с помощью uvicorn на адресе 127.0.0.1 и порту 8000 с автоматической перезагрузкой при изменениях в коде.