from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler, Updater

WAIT_TAKE, WAIT_TYPE_WATER, WAIT_TYPE_ROPES, WAIT_TYPE_EVERYDAY_LIFE, WAIT_TYPE_MEDICINE = range(5)


def ask_take(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Вода', callback_data='Вода'),
         InlineKeyboardButton('Веревки', callback_data='Веревки')],
        [InlineKeyboardButton('Быт', callback_data='Быт'),
         InlineKeyboardButton('Медицина', callback_data='Медицина')]
    ]

    take = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Какое направление Вас интересует?'
    update.message.reply_text(text, reply_markup=take)

    return WAIT_TAKE


def get_take(update: Update, context: CallbackContext):

    query = update.callback_query
    query.answer()
    if query.data == 'Вода':
        return ask_type_water(update, context)
    elif query.data == 'Веревки':
        return ask_type_ropes(update, context)
    elif query.data == 'Быт':
        return ask_type_everyday_life(update, context)
    elif query.data == 'Медицина':
        return ask_type_medicine(update, context)


def ask_type_water(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Снаряжение', callback_data='Снаряжение'),
         InlineKeyboardButton('Судна', callback_data='Судна')]
    ]

    query = update.callback_query
    type_water = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type_water)

    return WAIT_TYPE_WATER


def get_type_water(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


def ask_type_ropes(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Системы', callback_data='Системы'),
         InlineKeyboardButton('Веревки', callback_data='Веревки'),
         InlineKeyboardButton('Прочее', callback_data='Прочее')]
    ]

    query = update.callback_query
    type_ropes = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type_ropes)

    return WAIT_TYPE_ROPES


def get_type_ropes(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


def ask_type_everyday_life(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Ночлег', callback_data='Ночлег'),
         InlineKeyboardButton('Еда', callback_data='Еда'),
         InlineKeyboardButton('Прочее', callback_data='Прочее')]
    ]

    query = update.callback_query
    type_everyday_life = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type_everyday_life)

    return WAIT_TYPE_EVERYDAY_LIFE


def get_type_everyday_life(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


def ask_type_medicine(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Травмы', callback_data='Травмы'),
         InlineKeyboardButton('Обезболы', callback_data='Обезболы')]
    ]

    query = update.callback_query
    type_medicine = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type_medicine)

    return WAIT_TYPE_MEDICINE


def get_type_medicine(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


command_take_thing_handler = CommandHandler('take_thing', ask_take)
take_thing_handler = ConversationHandler(
    entry_points=[command_take_thing_handler],
    states={
        WAIT_TAKE: [CallbackQueryHandler(get_take), command_take_thing_handler],
        WAIT_TYPE_WATER: [CallbackQueryHandler(get_type_water), command_take_thing_handler],
        WAIT_TYPE_ROPES: [CallbackQueryHandler(get_type_ropes), command_take_thing_handler],
        WAIT_TYPE_EVERYDAY_LIFE: [CallbackQueryHandler(get_type_everyday_life), command_take_thing_handler],
        WAIT_TYPE_MEDICINE: [CallbackQueryHandler(get_type_medicine), command_take_thing_handler]
        },  # Состояние
    fallbacks=[]  # Отлов ошибок
)