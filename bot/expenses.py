"""Module which contains main operations with expenses."""
import datetime
import typing

import categories
import db
import exceptions
import message_parsing
from constants import MONTHS

CURRENT_MONTH_NUMBER = datetime.date.today().month


class Expense(typing.NamedTuple):
    """Class for representing expense."""

    amount: float
    category: str
    comment: str

    def __str__(self):
        """
        Return string representation of Expense.

        Returns:
            String representation of Expense
        """
        return f'{self.amount} {self.category} {self.comment}'


def add_expense(raw_message: str, context) -> None:
    """
    Add new expense.

    Args:
        raw_message: message which users prints in chat with bot.
        context: context of telegram bot.
    """
    expense = Expense(
        **message_parsing.parse_adding_message(raw_message),
    )
    db.insert('expense', {
        'amount': expense.amount,
        'category': expense.category,
        'comment': expense.comment,
        'author': context.user_data['author'],
    })


def look_expenses(raw_message: str) -> str:
    """
    Look for expenses and sum them by categories.

    Args:
        raw_message: message which users prints in chat with bot.

    Returns:
        Message containing sums of expenses divided by categories.
    """
    expenses = db.fetchall('expense', [
        'amount',
        'category',
        'created_at',
    ])
    expenses = list(
        filter(
            lambda expense: expense['created_at'].month == message_parsing.parse_month(raw_message),
            expenses,
        ),
    )
    if expenses:
        category_expensies = _calculate_expenses_for_month(expenses)
        output = '\n'.join(
            [
                f'{category}: {sum_expenses}'
                for category, sum_expenses in category_expensies
            ],
        )
    else:
        output = 'Не было никаких трат в этом месяце'
    return output


def get_history(raw_message: str) -> str:
    """
    Get history of expenses considered by message of user.

    Args:
        raw_message: message which users prints in chat with bot.

    Returns:
        String in row format where row represents one expense.
    """
    history_message = message_parsing.parse_history_message(raw_message)
    if len(history_message) == 1:
        word_type, word = _define_word_type(history_message[0])
        history = _build_history(**{word_type: word})
    else:
        history = _build_history(*history_message)
    output = '\n'.join([str(expense) for expense in history])
    return output if output else 'Не было никаких трат в этом месяце и категории'


def _calculate_expenses_for_month(expensies: typing.List[dict]) -> list:
    # TODO: Do the same but using sql sequence.
    categories_expensies = {
        category: 0 for category in categories.get_list_of_categories()
    }
    for expense in expensies:
        categories_expensies[expense['category']] += expense['amount']

    return list(categories_expensies.items())


def _define_word_type(word: str) -> typing.Tuple[str, typing.Union[int, str]]:
    word = word.lower()
    if word in MONTHS.keys():
        return 'month', MONTHS[word]
    elif word in categories.get_list_of_categories():
        return 'category', word
    raise exceptions.MessageException('Каво? Что это значит?\nПиши в формате: /history категория месяц')


def _build_history(
    category: typing.Optional[int] = None,
    month: int = CURRENT_MONTH_NUMBER,
) -> typing.List[Expense]:
    category = [category] if category else categories.get_list_of_categories()
    rows = db.fetchall('expense', [
        'amount',
        'category',
        'comment',
        'created_at',
    ])
    rows = filter(
        lambda expense: expense['created_at'].month == month and expense['category'] in category,
        rows,
    )
    return list(
        map(
            lambda expense: Expense(
                amount=expense['amount'],
                category=expense['category'],
                comment=expense['comment'],
            ),  # map to Expense object
            sorted(
                rows,
                key=lambda expense: expense['created_at'],
                reverse=True,
            ),  # sort by date
        ))
