"""Personal finance tracker: the entry point. Run with:  python main.py

This file only loads the data and runs the main menu. Each menu option is
handled by its own module, and the actual data work lives in separate files:

  Menus (ask the user for input, then call the logic below)
    menu_transactions.py   add, edit and delete transactions
    menu_categories.py     add, rename, delete and list categories
    menu_search.py         search transactions by date, category, type or text
    menu_goals.py          set, check and delete monthly goals
    menu_reports.py        all-time and single-month reports

  Logic (no input() calls, so they're easy to test)
    transaction.py   changing, searching and displaying transactions
    category.py      changing the category list
    goals.py         storing goals and working out progress
    summary.py       totals and reports

  Support
    helpers.py   input validation, menus, and date/money formatting
    storage.py   loading and saving the JSON files (data formats are described there)
    config.py    menu options, allowed values and limits

The loaded data (categories, transactions, goal_list) is passed into each menu.
Menus change it in place and save straight away, so main never needs to reload it.
"""

import config
import helpers
import menu_categories
import menu_goals
import menu_reports
import menu_search
import menu_transactions
import storage
import transaction


def show_main_menu(transactions: dict[int, dict], main_menu: str) -> None:
    """Print the transaction table with the main menu underneath."""
    print(transaction.build_transaction_table(transactions))
    print(main_menu)


def main() -> None:
    categories, transactions, goal_list = storage.load_file(config.DEFAULT_CATEGORIES)
    main_menu = helpers.build_menu(config.MAIN_OPTIONS)

    show_main_menu(transactions, main_menu)

    while True:
        # get_choice keeps asking until a valid number is entered,
        # and returns its position in config.MAIN_OPTIONS (starting at 0)
        menu_choice = helpers.get_choice(
            "Selected menu item: ", len(config.MAIN_OPTIONS)
        )

        if menu_choice == 0:
            menu_transactions.run(transactions, categories)
        elif menu_choice == 1:
            menu_categories.run(categories, transactions, goal_list)
        elif menu_choice == 2:
            menu_search.run(transactions, categories)
        elif menu_choice == 3:
            menu_goals.run(goal_list, transactions, categories)
        elif menu_choice == 4:
            menu_reports.run(transactions)
        else:
            break  # Exit

        # back from a submenu: show the (possibly updated) table and menu again
        show_main_menu(transactions, main_menu)


# Only start the app when this file is run directly, not when it's imported
# (for example by a test file)
if __name__ == "__main__":
    # Ctrl+C raises KeyboardInterrupt and Ctrl+D (Ctrl+Z on Windows) raises EOFError
    # while input() is waiting. Every change is saved as soon as it's made, so it's
    # safe to just exit quietly instead of showing a traceback.
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting, all changes are saved")
