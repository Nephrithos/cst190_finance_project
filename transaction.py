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
    """Add a transaction and return its new ID."""
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


def build_transaction_table(transactions: dict[int, dict]) -> str:
    """Return all transactions as a formatted table ready to print."""
    header = (
        f"{'ID':<4}  {'Date':<10}  {'Time':<5}  {'Type':<7}  "
        f"{'Category':<12}  {'Amount':>10}  {'Description':<20}"
    )
    line = "-" * len(header)

    table = line + "\n" + header + "\n" + line + "\n"

    if len(transactions) == 0:
        table += f"{'No transactions found':^{len(header)}}\n"
    else:
        for transaction_id in transactions:
            t = transactions[transaction_id]
            table += (
                f"{transaction_id:<4}  {t['date']:<10}  {t['time']:<5}  "
                f"{t['type']:<7}  {t['category']:<12.12}  "
                f"${t['amount']:>9.2f}  {t['description']:<20.20}\n"
            )

    table += line
    return table


def search_transactions(
    transactions: dict[int, dict], field: str, term: str, exact: bool = False
) -> dict[int, dict]:
    """Return the transactions whose field matches term.

    exact=True means the whole value must match (used for category and type).
    exact=False means term only has to appear somewhere in it (used for date and description).
    Both ignore upper/lower case.
    """
    results: dict[int, dict] = {}
    for transaction_id in transactions:
        value: str = str(transactions[transaction_id][field]).lower()
        if exact:
            found = value == term.lower()
        else:
            found = term.lower() in value
        if found:
            results[transaction_id] = transactions[transaction_id]
    return results
