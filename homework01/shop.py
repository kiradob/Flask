# Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал), 
# и дочерние шаблоны для страниц категорий товаров и отдельных товаров. 
# Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.

from flask import Flask, render_template, request

app = Flask(__name__)
# Здесь создаётся список warez с данными о товарах
warez = [
    ['group', 'name', 'desc', 'id'],
    ['Дом и Ремонт', 'Плитка в полосочку', 'Описание "Плитка в полосочку"', 'renov_dalleP'],
    ['Дом и Ремонт', 'Плитка в линеечку', 'Описание "Плитка в линеечку"', 'renov_dalleL'],
    ['Дом и Ремонт', 'Смеситель на кухню', 'Описание "Смеситель на кухню"', 'renov_smesK'],
    ['Дом и Ремонт', 'Смеситель в ванную комнату', 'Описание "Смеситель в ванную комнату"', 'renov_smesB'],
    ['"Электротехника"', 'УШМ', 'Описание "УШМ"', 'elet_anglegrinder'],
    ['Электротехника', 'Перфоратор', 'Описание "Перфоратор"', 'elet_perforator'],
]


def parse_wares_to_dict() -> list:
# Функция для преобразования списка warez в список словарей товаров
    res = []
    for val_lst_index in range(1, len(warez)):
        new_dict = {}
        for i in range(len(warez[0])):
            new_dict[warez[0][i]] = warez[val_lst_index][i]
        res.append(new_dict)
    return res

# Обработчик главной страницы
@app.route('/')
def index():
    context = {
        'title': 'Главная',
    }
    return render_template('index.html', **context)

# Обработчик страницы категорий товаров
@app.route('/categories/')
def categories():
    _warez = parse_wares_to_dict()

    context = {
        'title': 'Категории',
        'categories': [
            'Дом и Ремонт',
            'Электротехника',
        ],
        'warez': _warez,
    }
    return render_template('categories.html', **context)

# Обработчик страницы "О нас"
@app.route('/about/')
def about():
    context = {
        'title': 'О нас',
    }
    return render_template('about.html', **context)

# Обработчик страницы товара
@app.route('/warez/item/', methods=['GET', 'POST'])
def item():
    selected_item = request.args.get('selected_from_cats')
    _warez = parse_wares_to_dict()
    show_item = {}
    for item_dict in _warez:
        if item_dict['name'] == selected_item:
            show_item = dict(item_dict)
    context = {
        'title': 'Карточка товара',
        'selected': selected_item,
        'item': show_item,
    }
    return render_template('item.html', **context)


if __name__ == '__main__':
    app.run(debug=True)