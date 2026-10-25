def add_category(new_category: str, list_categories: list[str]) -> bool:
    for cat in list_categories:
        if cat.lower() == new_category.lower():
            return False
    list_categories.append(new_category)
    return True


def _find_index(category: str, list_categories: list[str]) -> int:
    """Return the index of category in the list, or -1 if it's not there."""
    for i in range(len(list_categories)):
        if list_categories[i].lower() == category.lower():
            return i
    return -1


def edit_category(old_name: str, new_name: str, list_categories: list[str]) -> bool:
    index = _find_index(old_name, list_categories)
    if index == -1:
        return False  # old name doesn't exist
    if _find_index(new_name, list_categories) not in (-1, index):
        return False  # new name already used by another category
    list_categories[index] = new_name
    return True


def remove_category(category: str, list_categories: list[str]) -> bool:
    index = _find_index(category, list_categories)
    if index == -1:
        return False
    list_categories.pop(index)
    return True
