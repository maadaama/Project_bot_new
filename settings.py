import pygsheets


class Item:
    def __init__(self, item_id, direction, category, item_type, state, notes, place):
        self.id = item_id
        self.direction = direction
        self.category = category
        self.type = item_type
        self.state = state
        self.notes = notes
        self.place = place


TABLE = '1QQMIHHH7G8uzqAw47xNHw_rKxLxRpDYP_663fSaUeug'  # ключ страницы инвентаризации
client = pygsheets.authorize(service_file='python-waldorf-4f0f67808d79.json')
table = client.open_by_key(TABLE)

cat_list = (2, 5)  # B5

items_columns = {
    'ид': 1,
    'направление': 4,
    'категория': 5,
    'тип': 6,
    'состояние': 7,
    'примечание': 8,
    'местоположение': 9,
}

info_columns = {
    'дата': 2,
    'ид': 3,
    'местоположение новое': 7,
    'состояние': 10,
    'примечания': 13,
    'кто обновил состояние': 16,
}

items_page = table.worksheet_by_title("Items")
info_page = table.worksheet_by_title("Обновления")
lists_page = table.worksheet_by_title("Списки")
