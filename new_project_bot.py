from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler, Updater, \
    MessageHandler, Filters
from key import TOKEN

WAIT_TAKE, WAIT_SEE_AVAILABILITY, WAIT_PUT, WAIT_TYPE, WAIT_TYPE1, WAIT_TYPE2, WAIT_TYPE3 = range(7)


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
    dispatcher.add_handler(CommandHandler('take', ask_take))
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
        return ask_type(update, context)
    elif query.data == 'Веревки':
        return ask_type1(update, context)
    elif query.data == 'Быт':
        return ask_type2(update, context)
    elif query.data == 'Медицина':
        return ask_type3(update, context)


def ask_type(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Снаряжение', callback_data='Снаряжение'),
         InlineKeyboardButton('Судна', callback_data='Судна')]
    ]

    query = update.callback_query
    type = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type)

    return WAIT_TYPE


def get_type(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


def ask_type1(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Системы', callback_data='Системы'),
         InlineKeyboardButton('Веревки', callback_data='Веревки'),
         InlineKeyboardButton('Прочее', callback_data='Прочее')]
    ]

    query = update.callback_query
    type1 = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type1)

    return WAIT_TYPE1


def get_type1(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


def ask_type2(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Ночлег', callback_data='Ночлег'),
         InlineKeyboardButton('Еда', callback_data='Еда'),
         InlineKeyboardButton('Прочее', callback_data='Прочее')]
    ]

    query = update.callback_query
    type2 = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type2)

    return WAIT_TYPE2


def get_type2(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


def ask_type3(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Травмы', callback_data='Травмы'),
         InlineKeyboardButton('Обезболы', callback_data='Обезболы')]
    ]

    query = update.callback_query
    type3 = InlineKeyboardMarkup(buttons)  # клавиатура - объект класса ReplyKeyboardMarkup
    text = 'Что Вас интересует?'
    query.edit_message_text(text, reply_markup=type3)

    return WAIT_TYPE3


def get_type3(update: Update, context: CallbackContext):
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
        WAIT_TYPE: [CallbackQueryHandler(get_type), command_take_handler],
        WAIT_TYPE1: [CallbackQueryHandler(get_type1), command_take_handler],
        WAIT_TYPE2: [CallbackQueryHandler(get_type2), command_take_handler],
        WAIT_TYPE3: [CallbackQueryHandler(get_type3), command_take_handler]
        },  # Состояние
    fallbacks=[]  # Отлов ошибок
)

if __name__ == '__main__':
    main()
