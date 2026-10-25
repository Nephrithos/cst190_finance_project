"""Settings shared across the app: allowed values, menu options and length limits.

Change things here (for example, add a default category or a menu option)
rather than inside the menu code. Menu option order matters: the menu modules
check which position was picked, so if you reorder a list, update its menu's run().
"""

# ---------- allowed values ----------

# Only used the first time the app runs (or if categories.json is damaged)
DEFAULT_CATEGORIES = ["Rent", "Food", "Salary"]

# Every transaction is one of these. Stored as the word, not the number picked.
EXPENSE_TYPES = ["expense", "income"]

# "spending limit" applies to one category; "saving" is income minus expenses for a month
GOAL_TYPES = ["spending limit", "saving"]

# ---------- limits ----------

CATEGORY_NAME_LENGTH = 15  # matches the Category column width in the transaction table
DESCRIPTION_LENGTH = 50

# ---------- menu options ----------

MAIN_OPTIONS = [
    "Transaction menu",
    "Category menu",
    "Search transactions",
    "Goals menu",
    "Reports",
    "Exit",
]
TRANSACTION_OPTIONS = ["Add transaction", "Edit transaction", "Delete transaction"]
CATEGORY_OPTIONS = [
    "Add category",
    "Edit category",
    "Delete category",
    "List categories",
]
GOAL_OPTIONS = ["Set goal", "Check goals", "Delete goal"]
REPORT_OPTIONS = ["All time", "Single month"]

# Field names here must match the keys of a transaction dictionary (see storage.py)
EDIT_FIELDS = ["amount", "type", "category", "date", "time", "description"]
SEARCH_FIELDS = ["date", "category", "type", "description"]

DATE_TIME_OPTIONS = ["Use current date and time", "Enter manually"]

SUBMENU_PROMPT = "Select menu option (leave blank for main menu): "
