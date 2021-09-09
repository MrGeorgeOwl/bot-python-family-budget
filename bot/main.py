"""Module for starting bot."""
import logging
import os
import pathlib

from telegram.ext import CommandHandler, Updater

import commands

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa: WPS323
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_DIR = os.path.join(pathlib.Path(__file__).parent)


func_to_model = [
    (commands.start, CommandHandler, {
        'command': 'start',
    }),
    (commands.add_expense, CommandHandler, {
        'command': 'add_expense',
    }),
    (commands.look_expenses, CommandHandler, {
        'command': 'look_expenses',
    }),
    (commands.look_history, CommandHandler, {
        'command': 'history',
    }),
    (commands.show_help, CommandHandler, {
        'command': 'help',
    }),
    (commands.show_categories, CommandHandler, {
        'command': 'categories',
    }),
]


def add_handlers(dispatcher):
    """
    Add handlers to dispatcher.

    Args:
        dispatcher: Dispatcher of telegram bot.
    """
    for func, model, kwargs in func_to_model:
        dispatcher.add_handler(model(callback=func, **kwargs))


if __name__ == '__main__':
    logger.info(f'BOT_TOKEN: {BOT_TOKEN}')
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    add_handlers(dispatcher)

    updater.start_polling()

    updater.idle()
