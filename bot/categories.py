import enum

class Category(enum.Enum):
    Chemistry = "Chemistry"
    Food = "Food"
    Pet = "Pet"

    mapping = {
        "Chemistry": Category.Chemistry,
        "Food": Category.Food,
        "Pet": Category.Pet,
    }

    @staticmethod
    def get_category(category_name: str) -> str:
        category = Category.mapping.get(category_name, None)
        if category:
            return category
        raise Exception("No such category")
