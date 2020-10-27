import enum
from typing import List


class Category(enum.Enum):
    Chemistry = "Chemistry"
    Food = "Food"
    Pet = "Pet"


_mapping = {
    "Chemistry": Category.Chemistry,
    "Food": Category.Food,
    "Pet": Category.Pet,
}


def get_category(category_name: str) -> Category:
    category = _mapping.get(category_name, None)
    if category:
        return category
    raise Exception("No such category")


def get_list_of_categories() -> List[str]:
    return _mapping.keys()
