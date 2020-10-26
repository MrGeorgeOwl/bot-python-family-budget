import os
import logging
import pathlib

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_DIR = os.path.join(pathlib.Path(__file__).parent)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=update.message.text)


func_to_model = [
    (start, CommandHandler, {
        "command": 'start',
    }),
    (echo, MessageHandler, {
        "filters": Filters.text & (~Filters.command),
    })
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
