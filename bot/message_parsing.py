"""Module which contains user message parsers."""
import datetime
import re
import typing

import categories
import exceptions
from constants import MONTHS


def parse_adding_message(raw_message: str) -> dict:
    """
    Parse user message for adding new expense.

    Args:
        raw_message: Message which users prints in chat with bot.

    Returns:
        A dict with information for creating Expense object.

    Raises:
        MessageException: User entered message of wrong format.
    """
    regexp_result = re.match(
        r'([\d+]*(,|.)?[\d]{,2})\s+(\w+)(\s+)?(.*)?',
        raw_message,
    )
    if not regexp_result:
        raise exceptions.MessageException('Каво?\nПиши так: 150 категория комментарий')

    try:
        category = categories.get_category(regexp_result.group(3).strip().lower()).value
    except exceptions.NoSuchCategory:
        raise exceptions.MessageException(
            'Каво?\nНе могу понять категорию \nДолжна быть одна из них: химия, еда или питомец',
        )

    return {
        "amount": float(regexp_result.group(1).replace(',', '.')),
        "category": category,
        "comment": regexp_result.group(5) if regexp_result.group(5) else '',
    }


def parse_month(raw_message: str) -> typing.Optional[int]:
    """
    Parse message which consists of month.

    Args:
        raw_message: Message which users prints in chat with bot.

    Returns:
        Integer representation of month if message exist else None.

    Raises:
        MessageException: User entered message of wrong format.
    """
    regexp_result = re.match(r'(\w+)', raw_message)
    if not regexp_result:
        return datetime.date.today().month
    month = regexp_result.group(1).lower()

    if month not in MONTHS.keys():
        raise exceptions.MessageException('Каво? Что это за месяц вообще?')

    month = MONTHS[month]
    if month > datetime.date.today().month:
        raise exceptions.MessageException('Каво? Ты назад в будущее решил отправиться?')

    return month


def parse_history_message(raw_message: str) -> list:
    """
    Parse message of user for history command.

    Args:
        raw_message: Message which users prints in chat with bot.

    Returns:
        A tuple with category and months if such values exist in user message.
    """
    regexp_result = re.match(r'(\w+)(\s+)?(\w+)?', raw_message)
    if not regexp_result:
        return []
    if not (regexp_result.group(3)):
        return [regexp_result.group(1)]
    return [regexp_result.group(1), MONTHS[regexp_result.group(3)]]
