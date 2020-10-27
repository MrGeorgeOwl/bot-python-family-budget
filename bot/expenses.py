import pdb
import re
from typing import Dict, NamedTuple, Optional, List
import datetime

import db
from categories import Category, get_category, get_list_of_categories
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
        return f"{amount} {category} {comment}"

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
    if not month:
        month = datetime.date.today().month

    if month > datetime.date.today().month:
        raise MessageException("Каво? Ты назад в будущее решил отправиться?")

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
        output = "\n".join([f"{category_expense[0]}: {category_expense[1]}"
                            for category_expense in category_expensies])
    else:
        output = "Не было никаких трат в этом месяце"
    return output
    


def _parse_adding_message(raw_message: str) -> Expense:
    regexp_result = re.match(
        r"([\d+]*(,|.)?[\d]{,2})\s+(\w+)\s+(\w+)", 
        raw_message)
    if not regexp_result:
        raise MessageException("Каво?\nПиши так: 150 категория комментарий")
    try:
        category = get_category(regexp_result.group(3).strip()).value
        return Expense(
            amount=float(regexp_result.group(1).replace(",", ".")),
            category=category,
            comment=regexp_result.group(4),
        )
    except Exception:
        raise MessageException("Каво?\nНе могу понять категорию "
                        "\nДолжна быть одна из них: Chemistry, Food или Pet")


def _parse_month(raw_message: str) -> Optional[int]:
    regexp_result = re.match(r"(\w+)", raw_message)
    if not regexp_result:
        return None
    month = regexp_result.group(1).lower()
    if month not in months.keys():
        raise MessageException("Каво? Что это за месяц вообще?")

    return months[month]


def _calculate_expenses_for_month(expensies: List[Dict]):
    categories_expensies = {category: 0 for category
                            in get_list_of_categories()}
    for expense in expensies:
        categories_expensies[expense["category"]] += expense['amount']
    
    return [item for item in categories_expensies.items()]