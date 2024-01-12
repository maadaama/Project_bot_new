from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler, Updater

WAIT_PUT = range(1)


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


command_put_thing_handler = CommandHandler('put_thing', ask_put)
put_thing_handler = ConversationHandler(
    entry_points=[command_put_thing_handler],
    states={
        WAIT_PUT: [CallbackQueryHandler(get_put), command_put_thing_handler]
        },  # Состояние
    fallbacks=[]  # Отлов ошибок
)