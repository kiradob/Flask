from datetime import date, timedelta # Импорт классов date и timedelta из модуля datetime для работы с датами и временными интервалами.
from random import choice, randint, uniform # Импорт функций для генерации случайных значений.
from passlib.hash import pbkdf2_sha256 # Импорт функции для хеширования паролей с использованием алгоритма PBKDF2-SHA256.
from decimal import Decimal # Импорт класса Decimal для работы с десятичными числами с фиксированной точностью.

from models import OrderStatus # Импорт перечисления OrderStatus из модуля models.
from database import db, users, items, orders # Импорт базы данных db и таблиц users, items, orders из модуля database.

# Константы, определяющие количество записей пользователей, товаров, заказов, минимальную и максимальную цену, 
# а также максимальный возраст заказа в днях.
USERS_IN_DB = 20
ITEMS_IN_DB = 40
ORDERS_IN_DB = 7
MIN_PRICE, MAX_PRICE = 1, 2_000_000
MAX_AGE_OF_ORDER_IN_DAYS = 40


async def populate(): # Функция populate(): Заполняет базу данных сгенерированными случайными записями для пользователей, товаров и заказов.
    for i in range(USERS_IN_DB):
        query = users.insert().values(firstname=f'Firstname_{i}', lastname=f'Lastname_{i}', email=f'mail{i}@mail.ru',
        # Генерируются пользователи с именем, фамилией, email и хешем пароля с помощью функции pbkdf2_sha256.hash().
                                      password_hash=pbkdf2_sha256.hash(f'pa$${i}word'))
        await db.execute(query)

    for i in range(ITEMS_IN_DB):
        query = items.insert().values(title=f'Title_{i}', description=f'Description_{i}',
                                      price=round(Decimal(uniform(MIN_PRICE, MAX_PRICE)), 2))
        await db.execute(query)

    for i in range(ORDERS_IN_DB):
        query = orders.insert().values(user_id=randint(1, USERS_IN_DB), item_id=randint(1, ITEMS_IN_DB),
# Генерируются заказы с произвольными идентификаторами пользователя и товара, датой в пределах последних MAX_AGE_OF_ORDER_IN_DAYS дней и
                                       # случайным статусом заказа из перечисления OrderStatus.
                                       date=date.today() - timedelta(days=randint(0, MAX_AGE_OF_ORDER_IN_DAYS)),
                                       status=choice(list(OrderStatus)))
        await db.execute(query)