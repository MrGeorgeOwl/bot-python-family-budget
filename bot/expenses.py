import re
from typing import Dict, List, NamedTuple, Optional, Tuple
import datetime

import db
from categories import get_category, get_list_of_categories
from exceptions import MessageException


months = {
    "январь": 1,
    "февраль": 2,
    "март": 3,
    "апрель": 4,
    "май": 5,
    "июнь": 6,
    "июль": 7,
    "август": 8,
    "сентябрь": 9,
    "октябрь": 10,
    "ноябрь": 11,
    "декабрь": 12,
}


class Expense(NamedTuple):
    amount: float
    category: str
    comment: str

    def __str__(self):
        return f"{self.amount} {self.category} {self.comment}"


def add_expense(raw_message: str, context) -> None:
    parsed_message = _parse_adding_message(raw_message)
    db.insert("expense", {
        "amount": parsed_message.amount,
        "category": parsed_message.category,
        "comment": parsed_message.comment,
        "author": context.user_data['author'],
    })


def look_expenses(raw_message: str) -> str:
    month = _parse_month(raw_message)
    expenses = db.fetchall("expense", [
        "amount",
        "category",
        "created_at"
    ])
    expenses = list(filter(
        lambda x: x['created_at'].month == month,
        expenses))
    if expenses:
        category_expensies = _calculate_expenses_for_month(expenses)
        output = "\n".join([f"{category}: {sum_expenses}"
                            for category, sum_expenses in category_expensies])
    else:
        output = "Не было никаких трат в этом месяце"
    return output


def get_history(raw_message: str) -> str:
    values = _parse_history_message(raw_message)
    if not values:
        history = _build_history()
    elif values[1]:
        history = _build_history(*values)
    elif not values[1]:
        value_name, value = _define_value(values[0])
        history = _build_history(**{value_name: value})
    else:
        raise MessageException("Каво? Что это значит?\n"
                               "Пиши в формате: /history категория месяц")
    output = "\n".join([str(expense) for expense in history])
    return output


def _parse_adding_message(raw_message: str) -> Expense:
    regexp_result = re.match(
        r"([\d+]*(,|.)?[\d]{,2})\s+(\w+)(\s+)?(.*)?",
        raw_message)
    if not regexp_result:
        raise MessageException("Каво?\nПиши так: 150 категория комментарий")
    try:
        category = get_category(regexp_result.group(3).strip().lower()).value
        return Expense(
            amount=float(regexp_result.group(1).replace(",", ".")),
            category=category,
            comment=regexp_result.group(5) if regexp_result.group(5) else "",
        )
    except Exception:
        raise MessageException("Каво?\nНе могу понять категорию "
                               "\nДолжна быть одна из них: химия, "
                               "еда или питомец")


def _parse_month(raw_message: str) -> Optional[int]:
    regexp_result = re.match(r"(\w+)", raw_message)
    if not regexp_result:
        return datetime.date.today().month
    month = regexp_result.group(1).lower()

    if month not in months.keys():
        raise MessageException("Каво? Что это за месяц вообще?")

    month = months[month]
    if month > datetime.date.today().month:
        raise MessageException("Каво? Ты назад в будущее решил отправиться?")

    return month


def _calculate_expenses_for_month(expensies: List[Dict]):
    # TODO: Do the same but using sql sequence.
    categories_expensies = {category: 0 for category
                            in get_list_of_categories()}
    for expense in expensies:
        categories_expensies[expense["category"]] += expense['amount']

    return [item for item in categories_expensies.items()]


def _parse_history_message(raw_message: str) -> Optional[Tuple[str]]:
    regexp_result = re.match(r"(\w+)(\s+)?(\w+)?", raw_message)
    if not regexp_result:
        return None
    if not(regexp_result.group(3)):
        return regexp_result.group(1), None
    else:
        return regexp_result.group(1), months[regexp_result.group(3)]


def _define_value(value: str) -> Tuple[str]:
    value = value.lower()
    if value in months.keys():
        return "month", months[value]
    elif value in get_list_of_categories():
        return "category", value
    else:
        raise MessageException("Каво? Что это значит?\n"
                               "Пиши в формате: /history категория месяц")


def _build_history(
    category: Optional[int] = None,
    month: int = datetime.date.today().month
) -> List[Expense]:
    category = [category] if category else get_list_of_categories()
    rows = db.fetchall('expense', [
        'amount',
        'category',
        'comment',
        'created_at'
    ])
    rows = filter(lambda x: x['created_at'].month == month
                  and x['category'] in category, rows)
    return list(
        map(
            lambda x: Expense(
                amount=x['amount'],
                category=x['category'],
                comment=x['comment'],
            ),  # map to Expense object
            sorted(rows, key=lambda x: x['created_at'],
                   reverse=True),  # sort by date
        ))
