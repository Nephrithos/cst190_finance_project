"""Transaction menu: add, edit and delete transactions.

Each function asks for its inputs (validated as they're typed, via helpers.py),
changes the transactions dictionary in place, and saves it straight away.
"""

import config
import helpers
import storage
import transaction


def add_transaction_entry(transactions: dict[int, dict], categories: list[str]) -> None:
    """Ask for every field of a new transaction, then add and save it."""
    amount = helpers.get_amount("Enter amount: ")
    expense_type = helpers.choose_item("Select expense type: ", config.EXPENSE_TYPES)
    expense_category = helpers.choose_item("Select category: ", categories)

    # Most transactions are logged as they happen, so "now" is the first option
    date_time_choice = helpers.choose_item(
        "Select date and time option: ", config.DATE_TIME_OPTIONS
    )
    if date_time_choice == "Enter manually":
        expense_date = helpers.get_date("Enter date (dd-mm-yyyy): ")
        expense_time = helpers.get_time("Enter time (hh:mm, 24 hour): ")
    else:
        expense_date, expense_time = helpers.get_date_time()

    expense_description = helpers.get_text(
        "Enter description (optional): ",
        allow_blank=True,
        max_length=config.DESCRIPTION_LENGTH,
    )

    new_id = transaction.add_transaction(
        transactions,
        amount,
        expense_type,
        expense_category,
        expense_date,
        expense_time,
        expense_description,
    )
    storage.write_file(transactions=transactions)
    print(f"Added transaction {new_id}")


def edit_transaction_entry(
    transactions: dict[int, dict], categories: list[str]
) -> None:
    """Ask which transaction and which field to change, then ask for the new value."""
    if len(transactions) == 0:
        print("No transactions to edit")
        return

    print(transaction.build_transaction_table(transactions))
    edit_id = helpers.get_transaction_id(
        "Transaction ID to edit (leave blank to cancel): ", transactions
    )
    if edit_id == -1:
        return

    field = helpers.choose_item("Select field to edit: ", config.EDIT_FIELDS)

    # Each field gets the same validation it had when the transaction was added
    if field == "amount":
        new_value = helpers.get_amount("New amount: ")
    elif field == "type":
        new_value = helpers.choose_item("Select expense type: ", config.EXPENSE_TYPES)
    elif field == "category":
        new_value = helpers.choose_item("Select category: ", categories)
    elif field == "date":
        new_value = helpers.get_date("New date (dd-mm-yyyy): ")
    elif field == "time":
        new_value = helpers.get_time("New time (hh:mm, 24 hour): ")
    else:
        new_value = helpers.get_text(
            "New description: ", allow_blank=True, max_length=config.DESCRIPTION_LENGTH
        )

    transaction.edit_transaction(transactions, edit_id, field, new_value)
    storage.write_file(transactions=transactions)
    print(f"Updated {field} for transaction {edit_id}")


def delete_transaction_entry(transactions: dict[int, dict]) -> None:
    """Ask which transaction to delete, confirm, then delete and save."""
    if len(transactions) == 0:
        print("No transactions to delete")
        return

    print(transaction.build_transaction_table(transactions))
    delete_id = helpers.get_transaction_id(
        "Transaction ID to delete (leave blank to cancel): ", transactions
    )
    if delete_id == -1:
        return

    # There's no undo, so always confirm
    if helpers.confirm(f"Delete transaction {delete_id}? (y/n): "):
        transaction.delete_transaction(transactions, delete_id)
        storage.write_file(transactions=transactions)
        print(f"Deleted transaction {delete_id}")
    else:
        print("Delete cancelled")


def run(transactions: dict[int, dict], categories: list[str]) -> None:
    """Show the transaction menu until the user leaves it blank."""
    while True:
        choice = helpers.select_from_list(
            config.SUBMENU_PROMPT, config.TRANSACTION_OPTIONS, allow_blank=True
        )
        if choice == -1:
            return
        if choice == 0:
            add_transaction_entry(transactions, categories)
        elif choice == 1:
            edit_transaction_entry(transactions, categories)
        else:
            delete_transaction_entry(transactions)
