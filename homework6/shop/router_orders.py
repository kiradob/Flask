from fastapi import APIRouter # Импорт класса APIRouter из модуля fastapi для создания путей API.

from models import Order, OrderIn # Импорт моделей Order и OrderIn из модуля models.
from database import db, orders # Импорт базы данных db и таблицы orders из модуля database.
from validator import DBTableEnum, validate_id # Импорт перечисления DBTableEnum и функции validate_id из модуля validator.

router = APIRouter(prefix="/orders", tags=["Orders"]) # Создание объекта router типа APIRouter с префиксом /orders и меткой "Orders".


@router.post("/", response_model=Order) # Декораторы маршрутизатора router:  Обработчик для создания нового заказа.

async def create_order(order_in: OrderIn):
    await validate_id(order_in.user_id, DBTableEnum.users)
    await validate_id(order_in.item_id, DBTableEnum.items)
    query = orders.insert().values(**order_in.dict())
    last_record_id = await db.execute(query)
    return {**order_in.dict(), "id": last_record_id}


@router.get("/", response_model=list[Order]) # Декораторы маршрутизатора router: Обработчик для чтения всех заказов.

async def read_orders():
    query = orders.select()
    return await db.fetch_all(query)


@router.get("/{order_id}", response_model=Order) # Декораторы маршрутизатора router: Обработчик для чтения одного заказа по идентификатору.

async def read_order(order_id: int):
    await validate_id(order_id, DBTableEnum.orders)
    query = orders.select().where(orders.c.id == order_id)
    return await db.fetch_one(query)


@router.put("/{order_id}", response_model=Order) # Декораторы маршрутизатора router: Обработчик для обновления заказа.

async def update_order(order_id: int, order_in: OrderIn):
    await validate_id(order_id, DBTableEnum.orders)
    await validate_id(order_in.user_id, DBTableEnum.users)
    await validate_id(order_in.item_id, DBTableEnum.items)
    query = orders.update().where(orders.c.id == order_id).values(**order_in.dict())
    await db.execute(query)
    return {**order_in.dict(), "id": order_id}


@router.delete("/{order_id}", response_model=dict) # Декораторы маршрутизатора router: Обработчик для удаления заказа.

async def delete_order(order_id: int):
    await validate_id(order_id, DBTableEnum.orders)
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {"message": "Заказ успешно удален"}

# Реализация операций CRUD (Create, Read, Update, Delete) для ресурса "orders":

# Создание нового заказа: Проверка идентификаторов пользователя и элемента, запрос на добавление нового заказа в таблицу orders
                        # и возврат созданного заказа вместе с присвоенным идентификатором.
# Получение всех заказов: Запрос на выбор всех заказов из таблицы orders.
# Получение одного заказа: Проверка идентификатора заказа, запрос на выбор заказа по заданному идентификатору из таблицы orders.
# Обновление заказа: Проверка идентификаторов заказа, пользователя и элемента, запрос на обновление заказа с заданным идентификатором 
                    # в таблице orders и возврат обновленного заказа.
# Удаление заказа: Проверка идентификатора заказа, запрос на удаление заказа с заданным идентификатором из таблицы orders 
# и возврат сообщения об успешном удалении.