"""Module which contains function for working with categories of expenses."""
import enum
from typing import KeysView

import exceptions


class Category(enum.Enum):
    """Class for containing possible expense categories."""

    chemistry = 'химия'
    food = 'еда'
    pet = 'питомец'


_mapping = {
    'химия': Category.chemistry,
    'еда': Category.food,
    'питомец': Category.pet,
}


def get_category(category_name: str) -> Category:
    """
    Get category.

    Args:
        category_name: Name of possible category.

    Returns:
        Category of expense.

    Raises:
        NoSuchCategory: User entered nonexistent category.
    """
    category = _mapping.get(category_name, None)
    if category:
        return category
    raise exceptions.NoSuchCategory('No such category')


def get_list_of_categories() -> KeysView[str]:
    """
    Get list of possible categories.

    Returns:
        KeysView of possible categories.
    """
    return _mapping.keys()
