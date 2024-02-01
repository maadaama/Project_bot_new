from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext
from key import TOKEN
from take_thing import take_thing_handler
from see_availability import see_availability_handler
from put_thing import put_thing_handler


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
    dispatcher.add_handler(take_thing_handler)
    dispatcher.add_handler(see_availability_handler)
    dispatcher.add_handler(put_thing_handler)

    # dispatcher.add_handler(MessageHandler(Filters.text, do_help))

    # Начать бесконечный опрос Телеграмма на предмет обновлений
    updater.start_polling()
    print(updater.bot.getMe())
    print('Бот запущен')
    updater.idle()


def do_help(update, context: CallbackContext):  # запускаем бота
    text = [
        'Привет!',
        'Я помогу тебе в работе со складом',
        'Для этого выбери одну из команд:',
        '/take_thing - взять вещь',
        '/see_availability - посмотреть наличие',
        '/put_thing - взять вещь',
    ]
    text = '\n'.join(text)  # Собираем строки в текст через разделитель
    update.message.reply_text(text)


def do_start(update, context: CallbackContext):  # запускаем бота
    text = [
        'Привет!',
        'Я помогу тебе в работе со складом',
        'Для этого выбери одну из команд:',
        '/take_thing - взять вещь',
        '/see_availability - посмотреть наличие',
        '/put_thing - взять вещь',
    ]
    text = '\n'.join(text)  # Собираем строки в текст через разделитель
    update.message.reply_text(text)


if __name__ == '__main__':
    main()
