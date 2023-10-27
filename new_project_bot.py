from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler, Updater, \
    MessageHandler, Filters
from key import TOKEN

WAIT_TAKE, WAIT_SEE_AVAILABILITY, WAIT_PUT, WAIT_TYPE_WATER, WAIT_TYPE_ROPES, WAIT_TYPE_EVERYDAY_LIFE = range(6)
WAIT_TYPE_MEDICINE = range(6, 6)


def main():
    """
    конфигуррирует и запускает бот
    """
    # Updater - объект, который ловит обновление из Телеграмма
    updater = Updater(token=TOKEN)

    # Диспетчер будет рапределять события по обработчикам
    dispatcher = updater.dispatcher

    # Добавляем обработчик события из Телеграмма
    dispatcher.add_handler(CommandHandler('start', do_start))
    dispatcher.add_handler(CommandHandler('help', do_help))
    dispatcher.add_handler(CommandHandler('register', register))
    # dispatcher.add_handler(CommandHandler('take', ask_take))
    dispatcher.add_handler(take_handler)
    dispatcher.add_handler(CommandHandler('see_availability', ask_see_availability))
    dispatcher.add_handler(CommandHandler('put', ask_put))

    dispatcher.add_handler(MessageHandler(Filters.text, do_help))

    # Начать бесконечный опрос Телеграмма на предмет обновлений
    updater.start_polling()
    print(updater.bot.getMe())
    print('Бот запущен')
    updater.idle()


def do_help(update, context: CallbackContext):  # запускаем бота
    text = [
        'Тестируем следующие функции:',
        '/take',
        '/see_availability',
        '/put'
    ]
    text = '\n'.join(text)  # Собираем строки в текст через разделитель
    update.message.reply_text(text)


def do_start(update, context: CallbackContext):  # запускаем бота
    text = [
        'Привет!',
        'Я помогу тебе в работе со складом',
        'Для этого, нажми на /register',
    ]
    text = '\n'.join(text)  # Собираем строки в текст через разделитель
    update.message.reply_text(text)


def register(update: Update, context: CallbackContext):
    return do_help(update, context)


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


def ask_see_availability(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Наличие на складе', callback_data='Наличие на складе'),
         InlineKeyboardButton('Наличие у людей', callback_data='Наличие у людей')]
    ]

    see_availability = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    update.message.reply_text(text, reply_markup=see_availability)

    return WAIT_SEE_AVAILABILITY


def get_see_availability(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


def ask_put(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('В хорошем состоянии', callback_data='В хорошем состоянии')],
        [InlineKeyboardButton('Сломана', callback_data='Сломана'),
         InlineKeyboardButton('Утеряна', callback_data='Утеряна')]
    ]

    see_availability = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    update.message.reply_text(text, reply_markup=see_availability)

    return WAIT_PUT


def get_put(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


command_take_handler = CommandHandler('take', ask_take)
take_handler = ConversationHandler(
    entry_points=[command_take_handler],
    states={
        WAIT_TAKE: [CallbackQueryHandler(get_take), command_take_handler],
        WAIT_SEE_AVAILABILITY: [CallbackQueryHandler(get_see_availability), command_take_handler],
        WAIT_PUT: [CallbackQueryHandler(get_put), command_take_handler],
        WAIT_TYPE_WATER: [CallbackQueryHandler(get_type_water), command_take_handler],
        WAIT_TYPE_ROPES: [CallbackQueryHandler(get_type_ropes), command_take_handler],
        WAIT_TYPE_EVERYDAY_LIFE: [CallbackQueryHandler(get_type_everyday_life), command_take_handler],
        WAIT_TYPE_MEDICINE: [CallbackQueryHandler(get_type_medicine), command_take_handler]
        },  # Состояние
    fallbacks=[]  # Отлов ошибок
)

if __name__ == '__main__':
    main()
