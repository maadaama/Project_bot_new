import logging
import datetime

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, ChatAction
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler, Updater

from tables import find_item, find_cat, change_item
WAIT_CATEGORY, WAIT_DIRECTION, WAIT_TYPE, WAIT_ITEM = range(4)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def ask_direction(update: Update, context: CallbackContext):
    logger.info('Вызвана функция ask_direction')
    buttons = [
        [InlineKeyboardButton('Вода', callback_data='Вода'),
         InlineKeyboardButton('Верёвки', callback_data='Верёвки')],
        [InlineKeyboardButton('Быт', callback_data='Быт'),
         InlineKeyboardButton('Медицина', callback_data='Медицина')]
    ]

    take = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Какое направление Вас интересует?'
    update.message.reply_text(text, reply_markup=take)

    return WAIT_DIRECTION


def get_direction(update: Update, context: CallbackContext):
    logger.info('Вызвана функция get_direction')
    query = update.callback_query
    query.answer()
    context.user_data['direction'] = query.data.lower()
    return ask_category(update, context)


def ask_category(update: Update, context: CallbackContext):
    logger.info('Вызвана функция ask_category')
    query = update.callback_query
    context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    cat = find_cat(query.data.lower())
    logger.info(f'Получена информация из таблицы: {cat}')
    buttons = []
    row = []
    for i in range(len(cat)):
        row.append(InlineKeyboardButton(cat[i], callback_data=cat[i]))
        if i % 3 == 1:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(buttons)
    text = 'Выберите категорию'
    query.edit_message_text(text, reply_markup=keyboard)

    return WAIT_CATEGORY


def get_category(update: Update, context: CallbackContext):
    logger.info('Вызвана функция get_category')
    query = update.callback_query
    query.answer('Один момент')
    context.user_data['items'] = find_item(query.data)
    return ask_type(update, context)


def ask_type(update: Update, context: CallbackContext):
    logger.info('Вызвана функция ask_type')
    query = update.callback_query
    items = context.user_data['items']
    context.user_data['items'] = [item for item in items if item.new_place == 'Склад']
    buttons = []
    row = []
    types = list(set([item.type for item in items]))

    for i in range(len(types)):
        row.append(InlineKeyboardButton(types[i], callback_data=types[i]))
        if len(row) % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(buttons)
    text = 'Выберите тип'
    query.edit_message_text(text, reply_markup=keyboard)

    return WAIT_TYPE


def get_type(update: Update, context: CallbackContext):
    logger.info('Вызвана функция get_type')
    query = update.callback_query
    query.answer()
    context.user_data['type'] = query.data
    return ask_item(update, context)


def ask_item(update: Update, context: CallbackContext):
    logger.info('Вызвана функция ask_item')
    query = update.callback_query
    items = context.user_data['items']
    buttons = []
    row = []
    text = []
    for i in range(len(items)):
        item = items[i]
        if item.type == query.data:
            context.user_data['items'].append(item)
            text.append(f'{item.id}: {item.type} {item.state} {item.notes}')
            row.append(InlineKeyboardButton(item.id, callback_data=i))
            if len(text) % 5 == 0:
                buttons.append(row)
                row = []
    if row:
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(buttons)
    text = '\n'.join(text)
    query.edit_message_text(text, reply_markup=keyboard)
    # context.bot.send_message(update.effective_chat.id, text, reply_markup=keyboard)

    return WAIT_ITEM


def get_item(update: Update, context: CallbackContext):
    logger.info('Вызвана функция get_item')
    query = update.callback_query
    query.answer()
    context.user_data['item'] = context.user_data['items'][int(query.data)]
    return register_movement(update, context)


def register_movement(update: Update, context: CallbackContext):
    query = update.callback_query
    place = 'Таня Каледа'
    date = str(datetime.date.today())
    context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    change_item(date, context.user_data['item'], place, place)
    text = 'Перемещение зарегистрировано'
    query.edit_message_text(text)
    return ConversationHandler.END


command_take_thing_handler = CommandHandler('take_thing', ask_direction)
take_thing_handler = ConversationHandler(
    entry_points=[command_take_thing_handler],
    states={
        WAIT_DIRECTION: [CallbackQueryHandler(get_direction), command_take_thing_handler],
        WAIT_CATEGORY: [CallbackQueryHandler(get_category), command_take_thing_handler],
        WAIT_TYPE: [CallbackQueryHandler(get_type), command_take_thing_handler],
        WAIT_ITEM: [CallbackQueryHandler(get_item), command_take_thing_handler],
        },  # Состояние
    fallbacks=[]  # Отлов ошибок
)
