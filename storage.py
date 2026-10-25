import json
import os

# Keep the data folder next to this file, so it works no matter where you run main.py from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transaction.json")
GOALS_FILE = os.path.join(DATA_DIR, "goals.json")


def _save_json(path: str, data) -> bool:
    """Write data to path, creating the data folder if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except PermissionError:
        print(f"Permission error: could not write {path}")
        return False


def _load_json(path: str, default):
    """Load JSON from path. If it is missing or broken, create it with the default."""
    if not os.path.exists(path):
        _save_json(path, default)
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Decoding error in {path}, creating new file")
        _save_json(path, default)
        return default
    except PermissionError:
        print(f"Permission error: could not read {path}, using defaults")
        return default


def write_file(
    categories: list[str] | None = None,
    transactions: dict[int, dict] | None = None,
    goals: list[dict] | None = None,
) -> bool:
    """Save whichever of categories/transactions/goals is passed in."""
    write_success = True
    if categories is not None:
        write_success = _save_json(CATEGORIES_FILE, categories) and write_success
    if transactions is not None:
        write_success = _save_json(TRANSACTIONS_FILE, transactions) and write_success
    if goals is not None:
        write_success = _save_json(GOALS_FILE, goals) and write_success
    return write_success


def load_file(
    default_categories: list[str],
) -> tuple[list[str], dict[int, dict], list[dict]]:
    """Load categories, transactions and goals, creating any file that doesn't exist."""
    categories = _load_json(CATEGORIES_FILE, list(default_categories))
    raw_transactions = _load_json(TRANSACTIONS_FILE, {})
    goal_list = _load_json(GOALS_FILE, [])

    # JSON always stores dict keys as strings, so turn them back into ints
    transactions = {int(k): v for k, v in raw_transactions.items()}
    return categories, transactions, goal_list
