"""Category list logic: adding, renaming and removing names.

Names are compared ignoring case, so "Food" and "food" count as the same
category. These functions only change the list; keeping transactions and
goals in step is handled in menu_categories.py.
"""


def _find_index(category: str, list_categories: list[str]) -> int:
    """Return the position of category in the list (ignoring case), or -1 if it's not there."""
    for i in range(len(list_categories)):
        if list_categories[i].lower() == category.lower():
            return i
    return -1


def add_category(new_category: str, list_categories: list[str]) -> bool:
    """Add a category. Returns False if it already exists."""
    if _find_index(new_category, list_categories) != -1:
        return False
    list_categories.append(new_category)
    return True


def edit_category(old_name: str, new_name: str, list_categories: list[str]) -> bool:
    """Rename a category. Returns False if old_name is missing or new_name is already used."""
    index = _find_index(old_name, list_categories)
    if index == -1:
        return False
    if _find_index(new_name, list_categories) not in (-1, index):
        return False
    list_categories[index] = new_name
    return True


def remove_category(category: str, list_categories: list[str]) -> bool:
    """Remove a category. Returns False if it doesn't exist."""
    index = _find_index(category, list_categories)
    if index == -1:
        return False
    list_categories.pop(index)
    return True
