"""Loading and saving the app's data as JSON files in the data/ folder.

The data/ folder and files are created automatically if they don't exist.
Data is checked on load: damaged entries are skipped, and a file that isn't
valid JSON is kept as <name>.bak so nothing is lost.

File formats:
  categories.json   a list of names
                    ["Rent", "Food"]

  transaction.json  transaction ID -> transaction
                    {"1": {"amount": 2550, "type": "expense", "category": "Food",
                           "date": "2026-10-25", "time": "13:30", "description": "Lunch"}}
                    amount is in whole cents (2550 = $25.50), so sums are exact.
                    type is "expense" or "income". IDs are saved as text by JSON
                    and turned back into ints on load.

  counters.json     the next ID to hand out
                    {"next_transaction_id": 5}
                    It only ever goes up, so a deleted transaction's ID is never reused.

  goals.json        a list of goals
                    [{"type": "spending limit", "amount": 20000,
                      "month": "2026-10", "category": "Food"}]
                    amount is in whole cents. type is "spending limit" or "saving".
                    Saving goals have category "".

Dates and months are saved year-first; see the date convention in helpers.py.
Categories are stored by name (not position), so they stay correct if the
category list changes.
"""

import json
import os

import config
import helpers
import transaction

# Keep the data folder next to this file, so it works no matter where you run main.py from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transaction.json")
GOALS_FILE = os.path.join(DATA_DIR, "goals.json")
COUNTERS_FILE = os.path.join(DATA_DIR, "counters.json")

TRANSACTION_FIELDS = ["amount", "type", "category", "date", "time", "description"]
GOAL_FIELDS = ["type", "amount", "month", "category"]


def _save_json(path: str, data) -> bool:
    """Write data to path, creating the data folder if needed."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except OSError:
        # OSError covers PermissionError, a full disk, a bad path and so on
        print(f"Could not save {path}")
        return False


def _load_json(path: str, default):
    """Load JSON from path. If it is missing, create it with the default.

    If it is broken, keep a copy as .bak (so nothing is lost) and start again with the default.
    """
    if not os.path.exists(path):
        _save_json(path, default)
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{path} is damaged, saved a copy as {path}.bak and started a new one")
        try:
            os.replace(path, path + ".bak")
        except OSError:
            pass
        _save_json(path, default)
        return default
    except OSError:
        print(f"Could not read {path}, using defaults")
        return default


def _to_cents(amount) -> int:
    """Return a stored amount in whole cents, or -1 if it isn't a valid amount.

    Amounts used to be saved as dollars in a float (25.5); they're now whole
    cents in an int (2550). A float is therefore an old dollar amount and is
    converted. bool is checked first because Python treats True as the int 1.
    """
    if isinstance(amount, bool):
        return -1
    if isinstance(amount, int):
        return amount
    if (
        isinstance(amount, float) and amount == amount
    ):  # amount == amount is False for nan
        return round(amount * 100)
    return -1


def _has_fields(item, fields: list[str]) -> bool:
    """Return True if item is a dictionary containing every field."""
    if not isinstance(item, dict):
        return False
    for field in fields:
        if field not in item:
            return False
    return True


def _check_categories(raw, default_categories: list[str]) -> list[str]:
    """Keep only text categories. Fall back to the defaults if none are left."""
    categories: list[str] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, str) and item.strip() != "":
                categories.append(item.strip())
    if len(categories) == 0:
        return list(default_categories)
    return categories


def _check_transactions(raw) -> dict[int, dict]:
    """Keep only complete transactions with a whole-number ID, a valid type and a positive amount."""
    transactions: dict[int, dict] = {}
    if not isinstance(raw, dict):
        return transactions
    skipped = 0
    repaired = 0
    for key in raw:
        item = raw[key]
        try:
            # JSON always stores dict keys as strings, so turn them back into ints
            transaction_id = int(key)
        except ValueError:
            skipped += 1
            continue
        if (
            _has_fields(item, TRANSACTION_FIELDS)
            and item["type"] in config.EXPENSE_TYPES
            and _to_cents(item["amount"]) > 0
        ):
            # repair amounts saved in the old dollars-as-float format
            if isinstance(item["amount"], float):
                item["amount"] = _to_cents(item["amount"])
                repaired += 1
            # repair dates saved in the old dd-mm-yyyy format
            if helpers.display_date(item["date"]) == item["date"]:
                fixed_date = helpers.convert_date(item["date"])
                if fixed_date != "":
                    item["date"] = fixed_date
                    repaired += 1
            transactions[transaction_id] = item
        else:
            skipped += 1
    if skipped > 0:
        print(f"Skipped {skipped} damaged transaction(s) in {TRANSACTIONS_FILE}")
    if repaired > 0:
        print(f"Converted {repaired} old-format date(s) or amount(s) to the new format")
        _save_json(TRANSACTIONS_FILE, transactions)
    return transactions


def _check_goals(raw) -> list[dict]:
    """Keep only complete goals with a positive amount."""
    goal_list: list[dict] = []
    if not isinstance(raw, list):
        return goal_list
    repaired = 0
    for item in raw:
        if _has_fields(item, GOAL_FIELDS) and _to_cents(item["amount"]) > 0:
            # repair amounts saved in the old dollars-as-float format
            if isinstance(item["amount"], float):
                item["amount"] = _to_cents(item["amount"])
                repaired += 1
            goal_list.append(item)
    if repaired > 0:
        _save_json(GOALS_FILE, goal_list)
    return goal_list


def _check_counters(raw, transactions: dict[int, dict]) -> dict[str, int]:
    """Return the ID counter, never lower than one past the highest ID in use.

    The check protects against a missing or hand-edited counters.json
    handing out an ID that already exists.
    """
    saved = 1
    if isinstance(raw, dict) and isinstance(raw.get("next_transaction_id"), int):
        saved = raw["next_transaction_id"]
    smallest_safe = transaction.highest_id(transactions) + 1
    if saved < smallest_safe:
        saved = smallest_safe
    return {"next_transaction_id": saved}


def write_file(
    categories: list[str] | None = None,
    transactions: dict[int, dict] | None = None,
    goals: list[dict] | None = None,
    counters: dict[str, int] | None = None,
) -> bool:
    """Save whichever of categories/transactions/goals/counters is passed in.

    Returns False if anything failed to save. Callers must check this and
    warn the user (see config.SAVE_FAILED).
    """
    write_success = True
    if categories is not None:
        write_success = _save_json(CATEGORIES_FILE, categories) and write_success
    if transactions is not None:
        write_success = _save_json(TRANSACTIONS_FILE, transactions) and write_success
    if goals is not None:
        write_success = _save_json(GOALS_FILE, goals) and write_success
    if counters is not None:
        write_success = _save_json(COUNTERS_FILE, counters) and write_success
    return write_success


def load_file(
    default_categories: list[str],
) -> tuple[list[str], dict[int, dict], list[dict], dict[str, int]]:
    """Load and check categories, transactions, goals and the ID counter.

    Any file that doesn't exist is created with a default.
    """
    categories = _check_categories(
        _load_json(CATEGORIES_FILE, list(default_categories)), default_categories
    )
    transactions = _check_transactions(_load_json(TRANSACTIONS_FILE, {}))
    goal_list = _check_goals(_load_json(GOALS_FILE, []))
    counters = _check_counters(
        _load_json(COUNTERS_FILE, {"next_transaction_id": 1}), transactions
    )
    return categories, transactions, goal_list, counters
