# Импорт необходимых модулей и классов для работы с типами данных, перечислениями и валидацией данных.

from decimal import Decimal
from datetime import date
from enum import StrEnum
from pydantic import BaseModel, Field, EmailStr 


class UserIn(BaseModel): # Определение Pydantic-моделей для пользователей, товаров и заказов, которые содержат определенные поля с заданными условиями валидации.
    firstname: str = Field(min_length=2, max_length=35)
    lastname: str = Field(min_length=2, max_length=80)
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=8, max_length=128)


class User(BaseModel): # Определение Pydantic-моделей для пользователей, товаров и заказов, которые содержат определенные поля с заданными условиями валидации.
    id: int
    firstname: str = Field(min_length=2, max_length=35)
    lastname: str = Field(min_length=2, max_length=80)
    email: EmailStr = Field(max_length=128)
    password_hash: str


class ItemIn(BaseModel): # Определение Pydantic-моделей для пользователей, товаров и заказов, которые содержат определенные поля с заданными условиями валидации.
    title: str = Field(min_length=3, max_length=128)
    description: str = Field(min_length=3, max_length=512)
    price: Decimal = Field(gt=0, le=1_000_000)


class Item(ItemIn): # Определение Pydantic-моделей для пользователей, товаров и заказов, которые содержат определенные поля с заданными условиями валидации.
    id: int


class OrderStatus(StrEnum): #  Определение перечисления OrderStatus с различными статусами заказов, представленными строковыми значениями.
    COMPLETED = 'выполнен'
    RECEIVED = 'получен'
    NEW = 'новый'
    UPDATED = 'обновлен'
    READY_TO_SHIP = 'подготовлен к отгрузке'
    PAY_AWAIT = 'ожидает оплаты'
    EXPIRED = 'истекший'
    CANCELED = 'отменен'
    PAY_RECEIVED = 'оплачен'
    SHIPPED = 'отправлен'
    CONFIRMED = 'подтвержден'
    ISSUED = 'выдан'
    


class OrderIn(BaseModel, use_enum_values=True): # Определение Pydantic-моделей для пользователей, товаров и заказов, которые содержат определенные поля с заданными условиями валидации.
    user_id: int = Field(gt=0)
    item_id: int = Field(gt=0)
    date: date
    status: OrderStatus # Использование перечисления OrderStatus для поля статуса заказа, указывая, что это поле должно принимать только определенные значения из перечисления.


class Order(OrderIn): # Определение Pydantic-моделей для пользователей, товаров и заказов, которые содержат определенные поля с заданными условиями валидации.
    id: int # Добавление поля id к модели заказа для хранения идентификатора заказа.