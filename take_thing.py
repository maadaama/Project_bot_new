from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, ChatAction
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler, Updater

from tables import find_item, find_cat
WAIT_CATEGORY, WAIT_DIRECTION = range(2)


def ask_direction(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Вода', callback_data='Вода'),
         InlineKeyboardButton('Веревки', callback_data='Веревки')],
        [InlineKeyboardButton('Быт', callback_data='Быт'),
         InlineKeyboardButton('Медицина', callback_data='Медицина')]
    ]

    take = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Какое направление Вас интересует?'
    update.message.reply_text(text, reply_markup=take)

    return WAIT_DIRECTION


def get_direction(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data['direction'] = query.data.lower()
    return ask_category(update, context)


def ask_category(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    cat = find_cat(query.data.lower())
    buttons = []
    row = []
    for i in range(len(cat)):
        row.append(InlineKeyboardButton(cat[i], callback_data=cat[i]))
        if i % 3 == 1:
            buttons.append(row)
            row = []
    keyboard = InlineKeyboardMarkup(buttons)
    text = 'Выберите категорию'
    query.edit_message_text(text, reply_markup=keyboard)

    return WAIT_CATEGORY


def get_category(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer('Один момент')
    context.user_data['items'] = find_item(query.data)


def ask_type(update: Update, context: CallbackContext):
    query = update.callback_query
    items = context.user_data['items']
    context.user_data['items'] = []
    buttons = []
    row = []

    for i in range(len(items)):
        item = items[i]
        if item.place == 'Склад':
            context.user_data['items'].append(item)
            row.append(InlineKeyboardButton(item.type, callback_data=item.type))
            if len(row) % 3 == 0:
                buttons.append(row)
                row = []
    if row:
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(buttons)
    text = 'Выберите тип'
    query.edit_message_text(text, reply_markup=keyboard)


def get_type(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data['type'] = query.data
    return ask_item(update, context)


def ask_item(update: Update, context: CallbackContext):
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
            row.append(InlineKeyboardButton(item.id, callback_data=item.id))
            if len(text) % 5 == 0:
                buttons.append(row)
                row = []
    if row:
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(buttons)
    text = '\n'.join(text)
    query.edit_message_text(text, reply_markup=keyboard)
    # context.bot.send_message(update.effective_chat.id, text, reply_markup=keyboard)





command_take_thing_handler = CommandHandler('take_thing', ask_direction)
take_thing_handler = ConversationHandler(
    entry_points=[command_take_thing_handler],
    states={
        WAIT_DIRECTION: [CallbackQueryHandler(get_direction), command_take_thing_handler],
        WAIT_CATEGORY: [CallbackQueryHandler(get_category), command_take_thing_handler],
        },  # Состояние
    fallbacks=[]  # Отлов ошибок
)
