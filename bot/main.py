import os
import logging
import pathlib

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import expenses
from exceptions import MessageException

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_DIR = os.path.join(pathlib.Path(__file__).parent)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, я бот для учета расходов\n"
        "Вот мои команды\n"
        "/add_expense 150 категория комментарий\n"
        " - добавляет новую трату в размере 150 рублей с\n"
        " заданным комментарием\n"
        "/look_expenses (месяц)\n"
        " - выводит общую сумму траты по категориям за\n"
        " заданный месяц"
        " * месяц опционален, если не выбран, то будут\n"
        " выведены траты за текущий месяц\n"
        "/history (категория) (месяц)\n" 
        " - выводит историю в виде списка трат в виде\n"
        " сумма категория кто?\n"
        " * категория опциональна, если не выбрана, то\n"
        " буду выведены все траты всех категорий\n"
        " * месяц опционален, если не выбран, то будут\n"
        " выведены траты за текущий месяц\n"
        " /help\n"
        " - выводит доступные команды\n")


def add_expense(update, context):
    message = " ".join(update.message.text.split()[1:])
    context.user_data['author'] = update.effective_user.first_name
    try:
        expenses.add_expense(message, context)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Трата была добавлена")
    except MessageException as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(e))
    except Exception as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Что-то пошло не так")
        logger.error(e)


def look_expenses(update, context):
    message = message = " ".join(update.message.text.split()[1:])
    try:
        message = expenses.look_expenses(message)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message)
    except MessageException as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(e))
    except Exception as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Что-то пошло не так")
        logger.error(e)
        


func_to_model = [
    (start, CommandHandler, {
        "command": 'start',
    }),
    (add_expense, CommandHandler, {
        'command': 'add_expense',
    }),
    (look_expenses, CommandHandler, {
        'command': 'look_expenses',
    }),
]


def add_handlers(dispatcher):
    for func, model, kwargs in func_to_model:
        dispatcher.add_handler(model(callback=func, **kwargs))


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    add_handlers(dispatcher)

    updater.start_polling()


if __name__ == "__main__":
    main()
