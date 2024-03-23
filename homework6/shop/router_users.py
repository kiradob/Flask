from fastapi import APIRouter # Импорт класса APIRouter из модуля fastapi для создания путей API.
from passlib.hash import pbkdf2_sha256 # Импорт функции хеширования pbkdf2_sha256 из модуля passlib.hash для безопасного хранения паролей.

from models import User, UserIn # Импорт моделей User и UserIn из модуля models.
from database import db, users # Импорт базы данных db и таблицы users из модуля database.
from validator import DBTableEnum, validate_id # Импорт перечисления DBTableEnum и функции validate_id из модуля validator.

router = APIRouter(prefix="/users", tags=["Users"]) # Создание объекта router типа APIRouter с префиксом /users и меткой "Users".


@router.post("/", response_model=User) # Декораторы маршрутизатора router: Обработчик для создания нового пользователя.

async def create_user(user_in: UserIn):
    user_to_db = user_in.dict().copy()
    user_to_db.setdefault('password_hash', pbkdf2_sha256.hash(user_to_db.pop('password')))
    query = users.insert().values(**user_to_db)
    last_record_id = await db.execute(query)
    return {**user_to_db, "id": last_record_id}


@router.get("/", response_model=list[User]) # Декораторы маршрутизатора router: Обработчик для чтения всех пользователей.

async def read_users():
    query = users.select()
    return await db.fetch_all(query)


@router.get("/{user_id}", response_model=User) # Декораторы маршрутизатора router: Обработчик для чтения одного пользователя по идентификатору.

async def read_user(user_id: int):
    await validate_id(user_id, DBTableEnum.users)
    query = users.select().where(users.c.id == user_id)
    return await db.fetch_one(query)


@router.put("/{user_id}", response_model=User) # Декораторы маршрутизатора router: Обработчик для обновления информации о пользователе.

async def update_user(user_id: int, user_in: UserIn):
    await validate_id(user_id, DBTableEnum.users)
    user_to_db = user_in.dict().copy()
    user_to_db.setdefault('password_hash', pbkdf2_sha256.hash(user_to_db.pop('password')))
    query = users.update().where(users.c.id == user_id).values(**user_to_db)
    await db.execute(query)
    return {**user_to_db, "id": user_id}


@router.delete("/{user_id}", response_model=dict) # Декораторы маршрутизатора router: Обработчик для удаления пользователя.

async def delete_user(user_id: int):
    await validate_id(user_id, DBTableEnum.users)
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {"message": "Пользователь успешно удален"}

# Реализация операций CRUD (Create, Read, Update, Delete) для ресурса "users":

# Создание нового пользователя: Хэширование пароля пользователя с использованием pbkdf2_sha256, 
                                # добавление пользователя в базу данных и возврат информации о созданном пользователе с присвоенным идентификатором.
# Получение всех пользователей: Запрос на выбор всех пользователей из таблицы users.
# Получение одного пользователя: Проверка идентификатора пользователя, запрос на выбор данных пользователя 
                                # с заданным идентификатором из таблицы users.
# Обновление информации о пользователе: Хэширование нового пароля пользователя, обновление данных пользователя в базе данных 
                                    # и возврат обновленной информации о пользователе.
# Удаление пользователя: Проверка идентификатора пользователя, запрос на удаление пользователя с заданным идентификатором из таблицы users
                        # и возврат сообщения об успешном удалении.