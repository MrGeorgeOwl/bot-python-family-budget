import os
import logging
from commands import func_to_model

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

def add_handlers(dispatcher):
    for func, command_str, model in func_to_model:
        dispatcher.add_handler(model(command_str, func))

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    add_handlers(dispatcher)

    updater.start_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
