from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler, Updater

WAIT_SEE_AVAILABILITY = range(1)


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


command_see_availability_handler = CommandHandler('see_availability', ask_see_availability)
see_availability_handler = ConversationHandler(
    entry_points=[command_see_availability_handler],
    states={
        WAIT_SEE_AVAILABILITY: [CallbackQueryHandler(get_see_availability), command_see_availability_handler]
        },  # Состояние
    fallbacks=[]  # Отлов ошибок
)
