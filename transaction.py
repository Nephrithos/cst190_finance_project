"""Transaction logic: adding, editing, deleting, searching and displaying.

Transactions are stored as {ID: transaction dictionary}; storage.py describes
the fields. These functions change the dictionary passed in but never ask for
input or save to disk. The menus do that, so the logic can be tested on its own.
"""

import helpers


def _next_id(transactions: dict[int, dict]) -> int:
    """Return one higher than the biggest existing ID, or 1 if there are none."""
    highest = 0
    for transaction_id in transactions:
        if transaction_id > highest:
            highest = transaction_id
    return highest + 1


def add_transaction(
    transactions: dict[int, dict],
    amount: float,
    expense_type: str,
    category: str,
    date: str,
    time: str,
    description: str,
) -> int:
    """Add a transaction and return its new ID. date must be yyyy-mm-dd."""
    new_id = _next_id(transactions)
    transactions[new_id] = {
        "amount": amount,
        "type": expense_type,
        "category": category,
        "date": date,
        "time": time,
        "description": description,
    }
    return new_id


def edit_transaction(
    transactions: dict[int, dict], transaction_id: int, field: str, new_value
) -> bool:
    """Change one field of a transaction. Returns False if the ID or field doesn't exist."""
    if transaction_id not in transactions:
        return False
    if field not in transactions[transaction_id]:
        return False
    transactions[transaction_id][field] = new_value
    return True


def delete_transaction(transactions: dict[int, dict], transaction_id: int) -> bool:
    """Delete a transaction. Returns False if the ID doesn't exist."""
    if transaction_id not in transactions:
        return False
    del transactions[transaction_id]
    return True


def rename_category(
    transactions: dict[int, dict], old_name: str, new_name: str
) -> None:
    """Update every transaction using old_name to use new_name instead."""
    for transaction_id in transactions:
        if transactions[transaction_id]["category"] == old_name:
            transactions[transaction_id]["category"] = new_name


def category_in_use(transactions: dict[int, dict], category: str) -> bool:
    """Return True if any transaction uses this category."""
    for transaction_id in transactions:
        if transactions[transaction_id]["category"] == category:
            return True
    return False


def search_transactions(
    transactions: dict[int, dict], field: str, term: str, exact: bool = False
) -> dict[int, dict]:
    """Return the transactions whose field matches term.

    exact=True means the whole value must match (used for category and type).
    exact=False means term only has to appear in it (used for date and description).
    Both ignore upper/lower case.
    """
    results: dict[int, dict] = {}
    for transaction_id in transactions:
        value = str(transactions[transaction_id][field]).lower()
        if exact:
            found = value == term.lower()
        else:
            found = term.lower() in value
        if found:
            results[transaction_id] = transactions[transaction_id]
    return results


def sorted_ids(transactions: dict[int, dict]) -> list[int]:
    """Return the transaction IDs ordered by date, then time (oldest first).

    Dates are saved as yyyy-mm-dd and times as hh:mm, so sorting them as text
    puts them in the right order. Python sorts tuples by the first item,
    then the second, and so on.
    """
    rows: list[tuple[str, str, int]] = []
    for transaction_id in transactions:
        t = transactions[transaction_id]
        rows.append((t["date"], t["time"], transaction_id))
    rows.sort()

    ids: list[int] = []
    for row in rows:
        ids.append(row[2])
    return ids


def build_transaction_table(transactions: dict[int, dict]) -> str:
    """Return the transactions as a table sorted by date and time, ready to print."""
    header = (
        f"{'ID':<4}  {'Date':<10}  {'Time':<5}  {'Type':<7}  "
        f"{'Category':<15}  {'Amount':>12}  {'Description':<20}"
    )
    line = "-" * len(header)

    table = line + "\n" + header + "\n" + line + "\n"

    if len(transactions) == 0:
        table += f"{'No transactions found':^{len(header)}}\n"
    else:
        for transaction_id in sorted_ids(transactions):
            t = transactions[transaction_id]
            table += (
                f"{transaction_id:<4}  {helpers.display_date(t['date']):<10}  "
                f"{t['time']:<5}  {t['type']:<7}  {t['category']:<15.15}  "
                f"{helpers.format_money(t['amount']):>12}  {t['description']:<20.20}\n"
            )

    table += line
    return table
