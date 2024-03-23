from fastapi import HTTPException # Импорт класса HTTPException из модуля fastapi для обработки исключений HTTP.
from enum import Enum # Импорт класса Enum из модуля enum для определения перечислений.

from database import db, users, items, orders 


class DBTableEnum(Enum):
    users = 'users'
    items = 'items'
    orders = 'orders'


async def validate_id(id_to_find: int, db_table_name: DBTableEnum): # Асинхронная функция validate_id, которая принимает идентификатор 
                                                                    # и имя таблицы для проверки.
                                                                    # Функция динамически вызывает соответствующий валидатор по имени таблицы.
    validator_to_call = globals()[f'_validate_{db_table_name.value}_id']
    await validator_to_call(id_to_find)


async def _validate_users_id(id_in: int) -> None: # Асинхронные функции валидации идентификаторов для каждой таблицы:
                                                # Проверяет существование пользователя с заданным идентификатором в таблице users, используя запрос к базе данных.
    if len(await db.fetch_all(query=users.select().where(users.c.id == id_in))) == 0:
        raise HTTPException(status_code=422, detail=f'Пользователь с id={id_in} отсутствует в БД')


async def _validate_items_id(id_in: int) -> None: # Асинхронные функции валидации идентификаторов для каждой таблицы:
                                                # Проверяет существование товара с заданным идентификатором в таблице items.
    if len(await db.fetch_all(query=items.select().where(items.c.id == id_in))) == 0:
        raise HTTPException(status_code=422, detail=f'Товар с id={id_in} отсутствует в БД')


async def _validate_orders_id(id_in: int) -> None: # Асинхронные функции валидации идентификаторов для каждой таблицы:
                                                    # Проверяет существование заказа с заданным идентификатором в таблице orders.
    if len(await db.fetch_all(query=orders.select().where(orders.c.id == id_in))) == 0:
        raise HTTPException(status_code=422, detail=f'Заказ с id={id_in} отсутствует в БД')
    # В случае, если идентификатор не найден в соответствующей таблице, генерируется исключение HTTPException с кодом состояния 422 и детализацией,
    # указывающей на отсутствие записи с указанным идентификатором в базе данных.