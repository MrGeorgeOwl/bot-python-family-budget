"""Module which contains bot commands."""
import logging

import categories
import expenses
from exceptions import MessageException

logger = logging.getLogger(__name__)

START_MESSAGE = """
Привет, я бот для учета расходов
Вот мои команды
/add_expense 150 категория комментарий
    - добавляет новую трату в размере 150 рублей с
      заданным комментарием
/look_expenses (месяц)
    - выводит общую сумму траты по категориям за
      заданный месяц
      * месяц опционален, если не выбран, то будут
        выведены траты за текущий месяц
/history (категория) (месяц)
    - выводит историю в виде списка трат в виде
      сумма категория кто?
      * категория опциональна, если не выбрана, то
      буду выведены все траты всех категорий
      * месяц опционален, если не выбран, то будут
        выведены траты за текущий месяц
/categories
    - выводит доступные категории
/help
    - выводит доступные команды
"""

HELP_MESSAGE = """
Вот мои команды
/add_expense 150 категория комментарий
    - добавляет новую трату в размере 150 рублей с
      заданным комментарием
/look_expenses (месяц)
    - выводит общую сумму траты по категориям за
      заданный месяц
      * месяц опционален, если не выбран, то будут
        выведены траты за текущий месяц
/history (категория) (месяц)
    - выводит историю в виде списка трат в виде
      сумма категория кто?
      * категория опциональна, если не выбрана, то
      буду выведены все траты всех категорий
      * месяц опционален, если не выбран, то будут
        выведены траты за текущий месяц
/categories
    - выводит доступные категории
/help
    - выводит доступные команды
"""


def start(update, context):
    """
    Show start bot message.

    Args:
        update: Represents an incoming update.
        context: Context passed to handler.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGE,
    )


def add_expense(update, context):
    """
    Add new expense.

    Args:
        update: Represents an incoming update.
        context: Context passed to handler.
    """
    message = _cut_command(update.message.text)
    context.user_data['author'] = update.effective_user.first_name
    response = 'Трата была добавлена'
    try:
        expenses.add_expense(message, context)
    except MessageException as exc:
        logger.error(exc)
        response = str(exc)
    except Exception as exc:
        response = 'Что-то пошло не так'
        logger.error(exc)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
    )


def look_expenses(update, context):
    """
    Show sum of expenses divided by categories.

    Args:
        update: Represents an incoming update.
        context: Context passed to handler.
    """
    message = _cut_command(update.message.text)
    try:
        response = expenses.look_expenses(message)
    except MessageException as exc:
        response = str(exc)
    except Exception as exc:
        logger.error(exc)
        response = 'Что-то пошло не так'

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
    )


def look_history(update, context):
    """
    Show history of expenses.

    Args:
        update: Represents an incoming update.
        context: Context passed to handler.
    """
    message = _cut_command(update.message.text)
    try:
        response = expenses.get_history(message)
    except MessageException as exc:
        response = str(exc)
    except Exception as exc:
        logger.error(exc)
        response = 'Что-то пошло не так'

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
    )


def show_categories(update, context):
    """
    Show message with possible categories.

    Args:
        update: Represents an incoming update.
        context: Context passed to handler.
    """
    try:
        response = (
            'Доступные категории: \n'
            + '\n'.join(categories.get_list_of_categories())
        )
    except MessageException as exc:
        response = str(exc)
    except Exception as exc:
        response = 'Что-то пошло не так'
        logger.error(exc)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
    )


def show_help(update, context):
    """
    Show help message.

    Args:
        update: Represents an incoming update.
        context: Context passed to handler.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_MESSAGE,
    )


def _cut_command(message: str) -> str:
    return ' '.join(message.split()[1:])
