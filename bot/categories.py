import enum
from typing import List


class Category(enum.Enum):
    Chemistry = "химия"
    Food = "еда"
    Pet = "питомец"


_mapping = {
    "химия": Category.Chemistry,
    "еда": Category.Food,
    "питомец": Category.Pet,
}


def get_category(category_name: str) -> Category:
    category = _mapping.get(category_name, None)
    if category:
        return category
    raise Exception("No such category")


def get_list_of_categories() -> List[str]:
    return _mapping.keys()
