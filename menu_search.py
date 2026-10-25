"""Search menu: find transactions by date, category, type or description.

Results are shown in the same table as the main screen. Searching doesn't
change any data, so nothing here saves.
"""

import config
import helpers
import transaction


def run(transactions: dict[int, dict], categories: list[str]) -> None:
    """Ask what to search by, show the matches, and repeat until left blank."""
    while True:
        choice = helpers.select_from_list(
            "Search by (leave blank for main menu): ",
            config.SEARCH_FIELDS,
            allow_blank=True,
        )
        if choice == -1:
            return
        search_field = config.SEARCH_FIELDS[choice]

        if search_field == "date":
            # The user types a day, month or year; get_search_date turns it into the
            # start of a saved date (yyyy-mm-dd, yyyy-mm or yyyy) to match against
            date_start = helpers.get_search_date(
                "Enter a day (dd-mm-yyyy), month (mm-yyyy) or year (yyyy): "
            )
            results = transaction.search_transactions(transactions, "date", date_start)

        elif search_field == "category":
            # exact=True so that searching "Food" doesn't also find "Seafood"
            chosen = helpers.choose_item("Select category: ", categories)
            results = transaction.search_transactions(
                transactions, "category", chosen, exact=True
            )

        elif search_field == "type":
            chosen = helpers.choose_item("Select expense type: ", config.EXPENSE_TYPES)
            results = transaction.search_transactions(
                transactions, "type", chosen, exact=True
            )

        else:
            # Description search matches any part of the text, ignoring case
            search_term = helpers.get_text(
                "Enter text to search for: ",
                allow_blank=False,
                max_length=config.DESCRIPTION_LENGTH,
            )
            results = transaction.search_transactions(
                transactions, "description", search_term
            )

        print(transaction.build_transaction_table(results))
