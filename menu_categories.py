"""Category menu: add, rename, delete and list categories.

Categories are referenced by name in transactions and goals, so renaming
updates those too, and deleting is refused while anything still uses the category.
"""

import category
import config
import goals
import helpers
import storage
import transaction


def add_category_entry(categories: list[str]) -> None:
    """Ask for a new category name and add it if it isn't already in the list."""
    new_category = helpers.get_text(
        "Name of the new category: ",
        allow_blank=False,
        max_length=config.CATEGORY_NAME_LENGTH,
    )
    # add_category compares names ignoring case, so "food" and "Food" count as the same
    if category.add_category(new_category, categories):
        storage.write_file(categories=categories)
        print(f"Added {new_category}")
    else:
        print(f"{new_category} already exists")


def edit_category_entry(
    categories: list[str], transactions: dict[int, dict], goal_list: list[dict]
) -> None:
    """Rename a category everywhere: the category list, transactions and goals."""
    old_name = helpers.choose_item("Number of category to edit: ", categories)
    new_name = helpers.get_text(
        f"New name for {old_name}: ",
        allow_blank=False,
        max_length=config.CATEGORY_NAME_LENGTH,
    )
    if category.edit_category(old_name, new_name, categories):
        transaction.rename_category(transactions, old_name, new_name)
        goals.rename_category(goal_list, old_name, new_name)
        storage.write_file(
            categories=categories, transactions=transactions, goals=goal_list
        )
        print(f"Renamed {old_name} to {new_name}")
    else:
        print(f"{new_name} already exists")


def delete_category_entry(
    categories: list[str], transactions: dict[int, dict], goal_list: list[dict]
) -> None:
    """Delete a category, unless it's the last one or something still uses it."""
    # Adding a transaction needs at least one category to pick from
    if len(categories) == 1:
        print("You need at least one category, add another before deleting this one")
        return

    remove_name = helpers.choose_item("Number of category to delete: ", categories)

    # Deleting a category in use would leave transactions or goals pointing at nothing
    if transaction.category_in_use(transactions, remove_name) or goals.category_in_use(
        goal_list, remove_name
    ):
        print(
            f"{remove_name} is used by transactions or goals, change or delete those first"
        )
        return

    if helpers.confirm(f"Delete {remove_name}? (y/n): "):
        category.remove_category(remove_name, categories)
        storage.write_file(categories=categories)
        print(f"Deleted {remove_name}")
    else:
        print("Delete cancelled")


def run(
    categories: list[str], transactions: dict[int, dict], goal_list: list[dict]
) -> None:
    """Show the category menu until the user leaves it blank."""
    while True:
        choice = helpers.select_from_list(
            config.SUBMENU_PROMPT, config.CATEGORY_OPTIONS, allow_blank=True
        )
        if choice == -1:
            return
        if choice == 0:
            add_category_entry(categories)
        elif choice == 1:
            edit_category_entry(categories, transactions, goal_list)
        elif choice == 2:
            delete_category_entry(categories, transactions, goal_list)
        else:
            print(helpers.build_menu(categories))
