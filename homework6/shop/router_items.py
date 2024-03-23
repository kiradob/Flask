from fastapi import APIRouter # Импорт класса APIRouter из модуля fastapi для создания путей API.

from models import Item, ItemIn # Импорт моделей Item и ItemIn из модуля models.
from database import db, items #  Импорт базы данных db и таблицы items из модуля database.
from validator import DBTableEnum, validate_id # Импорт перечисления DBTableEnum и функции validate_id из модуля validator.

router = APIRouter(prefix="/items", tags=["Items"]) # Создание объекта router типа APIRouter с префиксом /items и меткой "Items".


@router.post("/", response_model=Item) # Обработчик для создания нового элемента.

async def create_item(item_in: ItemIn):
    query = items.insert().values(**item_in.dict())
    last_record_id = await db.execute(query)
    return {**item_in.dict(), "id": last_record_id}


@router.get("/", response_model=list[Item]) # Обработчик для чтения всех элементов.

async def read_items():
    query = items.select()
    return await db.fetch_all(query)

 
@router.get("/{item_id}", response_model=Item) # Обработчик для чтения одного элемента по идентификатору.

async def read_item(item_id: int):
    await validate_id(item_id, DBTableEnum.items)
    query = items.select().where(items.c.id == item_id)
    return await db.fetch_one(query)


@router.put("/{item_id}", response_model=Item) # Обработчик для обновления элемента.

async def update_item(item_id: int, item_in: ItemIn):
    await validate_id(item_id, DBTableEnum.items)
    query = items.update().where(items.c.id == item_id).values(**item_in.dict())
    await db.execute(query)
    return {**item_in.dict(), "id": item_id}


@router.delete("/{item_id}", response_model=dict) # Обработчик для удаления элемента.

async def delete_item(item_id: int):
    await validate_id(item_id, DBTableEnum.items)
    query = items.delete().where(items.c.id == item_id)
    await db.execute(query)
    return {"message": "Товар успешно удален"}


# Реализация операций CRUD (Create, Read, Update, Delete) для ресурса "items":

# Создание нового элемента: Запрос на добавление нового элемента в таблицу items и возврат созданного элемента вместе с присвоенным идентификатором.
# Получение всех элементов: Запрос на выбор всех элементов из таблицы items.
# Получение одного элемента: Запрос на выбор элемента по заданному идентификатору из таблицы items.
# Обновление элемента: Запрос на обновление элемента с заданным идентификатором в таблице items и возврат обновленного элемента.
# Удаление элемента: Запрос на удаление элемента с заданным идентификатором из таблицы items и возврат сообщения об успешном удалении.