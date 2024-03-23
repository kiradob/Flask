from databases import Database # Загрузка класса Database из библиотеки databases, который обеспечивает абстракцию для работы с базами данных.
from sqlalchemy import MetaData, Table, Column, create_engine, ForeignKey, Date # Импорт необходимых компонентов SQLAlchemy для определения структуры базы данных.
from sqlalchemy import Integer, String, Enum, DECIMAL # Импорт необходимых компонентов SQLAlchemy для определения структуры базы данных.

from models import OrderStatus # Импорт класса OrderStatus из модуля models, который определяет статусы заказов.

DB_URL = "sqlite:///shop.db" # Определение URL-адреса базы данных SQLite, в которой будут создаваться таблицы.

db = Database(DB_URL) # Создание экземпляра Database с указанием URL базы данных.

metadata = MetaData() # Создание объекта MetaData для хранения метаданных таблиц.

users = Table(
    "users",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('firstname', String(35), nullable=False),
    Column('lastname', String(80), nullable=False),
    Column('email', String(128), nullable=False),
    Column('password_hash', String(128), nullable=False),
)

items = Table(
    "items",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(128), nullable=False),
    Column('description', String(512), nullable=True),
    Column('price', DECIMAL, nullable=False),
)

orders = Table(
    "orders",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('item_id', ForeignKey('items.id'), nullable=False),
    Column('date', Date, nullable=False),
    Column('status', Enum(OrderStatus), nullable=False),
)


engine = create_engine(DB_URL, connect_args={"check_same_thread": False}) # Создание движка SQLAlchemy для взаимодействия с базой данных SQLite, 
                                                                        #   с предоставлением параметра check_same_thread=False, 
                                                                        # что требуется для безопасной работы с SQLite в многопоточной среде.

metadata.create_all(engine) # Создание всех определенных таблиц в базе данных с помощью механизма метаданных и движка, что автоматически создаст таблицы с указанной структурой.