import pygsheets
from settings import items_page, info_page, items_columns, lists_page, cat_list, info_columns, Item


def find_cat(direction):
    result = []
    col = 0
    data_range = pygsheets.DataRange(start='B5', end='D24', worksheet=lists_page)  # TODO нужен рефакторинг
    for row in data_range:
        if row[col].value == direction:
            result.append(row[col+1].value)
        if not row[col].value:
            break

    return result


def find_item(category):
    result = []
    col = items_columns['категория'] - 1
    data_range = pygsheets.DataRange(start='A4', end='I50', worksheet=items_page)  # TODO нужен рефакторинг
    for row in data_range:
        val = row[col].value
        if val == category:
            params = []
            for i in items_columns.keys():
                params.append(row[items_columns[i] - 1].value)

            result.append(Item(*params))
        elif not val:
            break
    return result


def change_item(date, item_id, place):
    pass  # TODO прописать функцию


if __name__ == '__main__':
    columns = 'HKLO'

    # for row in range(4, 10):
    #     for col in range(5, 8):
    #         print(items_page.cell((row, col)).value, end=' ')
    #     print()

    print(find_cat('вода'))
    print(find_item('карабин'))

    # Открываем таблицу с помощью семейства методов open_<bla-bla-bla>
    #

    # # Select worksheet by id, index, title.
    # wks = sh.worksheet_by_title("my test sheet")
    #
    # # By any property
    # wks = sh.worksheet('index', 0)
    #
    # # Get a list of all worksheets
    # wks_list = sh.worksheets()
    #
    # # Or just
    # wks = sh[0]

    # sheet = table.worksheet_by_title('102 E120n')
    # print(table.worksheets())
    # print(sheet.url, sheet.title, sheet.index)
    #
    # sheet.update_value('E6', '30.01.2021')  # Записывает данные, как если бы пользователь вводил руками
    # sheet.update_value('E7', '30.02.2021', parse=True)  # Записывает именно строчку
