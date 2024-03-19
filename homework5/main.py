# Необходимо создать API для управления списком задач.
# Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
# API должен содержать следующие конечные точки:
#   ○ GET /tasks - возвращает список всех задач.
#   ○ GET /tasks/{id} - возвращает задачу с указанным идентификатором.
#   ○ POST /tasks - добавляет новую задачу.
#   ○ PUT /tasks/{id} - обновляет задачу с указанным идентификатором.
#   ○ DELETE /tasks/{id} - удаляет задачу с указанным идентификатором.
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.
from enum import Enum
from random import choice

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from uvicorn import run as uvi_run

app = FastAPI()
ID = 0
tasks = []


def _get_id() -> int:
    global ID
    ID += 1
    return ID

# Создаем перечисление для статуса задачи
class Status(str, Enum):
    TODO = 'не выполнена'
    DONE = 'выполнена'

# Модель данных для входных данных создания задачи
class TaskIn(BaseModel, use_enum_values=True):
    title: str
    description: str
    status: Status

# Модель данных для задачи
class Task(TaskIn, use_enum_values=True):
    id: int

# Генерируем задачи для начального заполнения
def _generate_tasks(qty: int = 10) -> None:
    tasks.extend([Task(id=_get_id(), title=f'Title_{i}', description=f'desc_{i}', status=choice(list(Status)))
                  for i in range(1, qty + 1)])

# Главная страница
@app.get('/', response_class=HTMLResponse)
async def index():
    return '<h3>Главная страница</h3>'

# Получение списка всех задач
@app.get('/tasks', response_model=list[Task])
async def get_tasks():
    if len(tasks) == 0:
        _generate_tasks()
    return tasks

# Получение задачи по идентификатору
@app.get('/tasks/{task_id}', response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail='Задача не найдена')

# Создание новой задачи
@app.post('/tasks', response_model=Task)
async def create_task(query: TaskIn):
    new_task = Task(id=_get_id(), title=query.title, description=query.description, status=query.status)
    tasks.append(new_task)
    return new_task

# Обновление задачи по идентификатору
@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, query: TaskIn):
    for task in tasks:
        if task.id == task_id:
            task.title = query.title
            task.description = query.description
            task.status = query.status
            return task
    raise HTTPException(status_code=404, detail='Задача не найдена')

# Удаление задачи по идентификатору
@app.delete('/tasks/{task_id}', response_model=dict)
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {'message': 'Успешное удаление задачи'}
    raise HTTPException(status_code=404, detail='Задача не найдена')

# Запуск приложения
if __name__ == '__main__':
    uvi_run('main:app', host='127.0.0.1', port=8000, reload=True)