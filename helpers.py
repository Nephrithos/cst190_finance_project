"""Shared helpers: menus, validated input, and date/money formatting.

Every get_... / choose_... function keeps asking until the input is valid,
so callers can use the result straight away without checking it again.

Date convention used across the app:
  users type   dd-mm-yyyy (dates)   mm-yyyy (months)
  saved as     yyyy-mm-dd           yyyy-mm
Year-first is saved because it sorts correctly as text and lets
"starts with 2026-10" find a whole month. display_date / display_month
convert back for showing to the user.
"""

import datetime


# ---------- menus ----------


def build_menu(options: list[str]) -> str:
    """Return a numbered menu on one line, e.g. "1: Rent  2: Food  "."""
    menu = ""
    for i in range(len(options)):
        menu += f"{i + 1}: {options[i]}  "
    return menu


def get_choice(prompt: str, number_of_options: int, allow_blank: bool = False) -> int:
    """Ask until the user enters a number from 1 to number_of_options.

    Returns the position in the list (starting at 0),
    or -1 if allow_blank is True and the user left it blank.
    """
    while True:
        entry = input(prompt).strip()
        if entry == "" and allow_blank:
            return -1
        try:
            number = int(entry)
        except ValueError:
            number = 0
        if 1 <= number <= number_of_options:
            return number - 1
        print(f"Enter a number from 1 to {number_of_options}")


def select_from_list(prompt: str, items: list[str], allow_blank: bool = False) -> int:
    """Show items as a numbered menu and ask until a valid one is picked.

    Returns the position in the list (starting at 0), or -1 if blank was allowed and entered.
    """
    if len(items) == 0:
        print("There is nothing to choose from")
        return -1
    print(build_menu(items))
    return get_choice(prompt, len(items), allow_blank)


def choose_item(prompt: str, items: list[str]) -> str:
    """Show items as a numbered menu and return the item picked (not its number).

    items must not be empty.
    """
    return items[select_from_list(prompt, items)]


def confirm(prompt: str) -> bool:
    """Ask a yes/no question until the user answers y or n."""
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y" or answer == "yes":
            return True
        if answer == "n" or answer == "no":
            return False
        print("Enter y or n")


# ---------- text and numbers ----------


def get_text(prompt: str, allow_blank: bool, max_length: int) -> str:
    """Ask for text until it is not too long (and not blank, unless blank is allowed)."""
    while True:
        text = input(prompt).strip()
        if text == "" and not allow_blank:
            print("This cannot be blank")
        elif len(text) > max_length:
            print(f"Keep it to {max_length} characters or fewer")
        else:
            return text


MAX_CENTS = 100_000_000_000  # $1,000,000,000.00, a sanity limit on one amount


def parse_cents(text: str) -> int:
    """Turn typed money such as "25", "25.5", ".50" or "$1,250.50" into whole cents.

    Returns -1 if it isn't a plain positive amount, and -2 if it has more than
    2 decimal places. The text is read digit by digit rather than through
    float(), so the result is exact (float("0.29") * 100 is 28.999999999999996).
    """
    text = text.strip().replace("$", "").replace(",", "")
    if text.count(".") > 1:
        return -1
    if "." in text:
        dollars, cents = text.split(".")
    else:
        dollars, cents = text, ""
    if dollars == "":
        dollars = "0"  # allows ".50"
    # isdecimal() rejects signs, spaces, "e" notation, "nan" and "inf"
    if not dollars.isdecimal() or (cents != "" and not cents.isdecimal()):
        return -1
    if len(cents) > 2:
        return -2
    return int(dollars) * 100 + int(cents.ljust(2, "0"))


def get_amount(prompt: str) -> int:
    """Ask until the user enters a positive amount with at most 2 decimal places.

    Returns the amount in whole cents ($25.50 -> 2550). Money is kept in
    cents everywhere so adding it up is exact.
    """
    while True:
        cents = parse_cents(input(prompt))
        if cents == -2:
            print("Use at most 2 decimal places")
        elif not 0 < cents <= MAX_CENTS:
            print("Enter an amount greater than 0, e.g. 25.50")
        else:
            return cents


def get_transaction_id(prompt: str, transactions: dict[int, dict]) -> int:
    """Ask until the user enters an ID that exists. Returns -1 if left blank."""
    while True:
        entry = input(prompt).strip()
        if entry == "":
            return -1
        try:
            transaction_id = int(entry)
        except ValueError:
            transaction_id = 0
        if transaction_id in transactions:
            return transaction_id
        print("Transaction not found, enter an ID from the table")


def format_money(cents: int) -> str:
    """Format whole cents as $1,234.50, with any minus sign in front of the $.

    Uses whole-number division, not float, so the cents printed are exact.
    """
    sign = "-" if cents < 0 else ""
    dollars, remainder = divmod(abs(cents), 100)
    return f"{sign}${dollars:,}.{remainder:02d}"


# ---------- dates and times ----------
# See the date convention at the top of this file.


def get_date_time() -> tuple[str, str]:
    """Return the current date (yyyy-mm-dd) and time (hh:mm)."""
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")
    return date, time


def _year_ok(date: datetime.datetime) -> bool:
    """Reject years that are almost certainly typos (e.g. 0026 or 20266)."""
    return 1900 <= date.year <= 2100


def convert_date(date_text: str) -> str:
    """Turn a dd-mm-yyyy date into yyyy-mm-dd. Returns "" if it isn't a valid date."""
    try:
        entered = datetime.datetime.strptime(date_text, "%d-%m-%Y")
    except ValueError:
        return ""
    if not _year_ok(entered):
        return ""
    return entered.strftime("%Y-%m-%d")


def get_date(prompt: str) -> str:
    """Ask until the user enters a valid dd-mm-yyyy date. Returns it as yyyy-mm-dd."""
    while True:
        date = convert_date(input(prompt).strip())
        if date != "":
            return date
        print("Enter a real date as dd-mm-yyyy, e.g. 25-10-2026")


def get_time(prompt: str) -> str:
    """Ask until the user enters a valid 24 hour time. Returns it as hh:mm."""
    while True:
        try:
            entered = datetime.datetime.strptime(input(prompt).strip(), "%H:%M")
            return entered.strftime("%H:%M")
        except ValueError:
            print("Enter a 24 hour time as hh:mm, e.g. 09:30 or 18:45")


def get_month(prompt: str) -> str:
    """Ask for a month as mm-yyyy. Blank means this month. Returns it as yyyy-mm."""
    while True:
        entry = input(prompt).strip()
        if entry == "":
            today, now_time = get_date_time()
            return today[:7]
        try:
            entered = datetime.datetime.strptime(entry, "%m-%Y")
            if _year_ok(entered):
                return entered.strftime("%Y-%m")
        except ValueError:
            pass
        print("Enter a month as mm-yyyy, e.g. 10-2026")


def get_search_date(prompt: str) -> str:
    """Ask for a day (dd-mm-yyyy), month (mm-yyyy) or year (yyyy).

    Returns the start of a saved date to search for: yyyy-mm-dd, yyyy-mm or yyyy.
    """
    while True:
        entry = input(prompt).strip()
        formats = [("%d-%m-%Y", "%Y-%m-%d"), ("%m-%Y", "%Y-%m"), ("%Y", "%Y")]
        for entry_format, saved_format in formats:
            try:
                entered = datetime.datetime.strptime(entry, entry_format)
                if _year_ok(entered):
                    return entered.strftime(saved_format)
            except ValueError:
                pass
        print("Enter a day (dd-mm-yyyy), month (mm-yyyy) or year (yyyy)")


def current_month_display() -> str:
    """Return this month as mm-yyyy, for showing in prompts."""
    today, now_time = get_date_time()
    return display_month(today[:7])


def display_date(saved_date: str) -> str:
    """Turn a saved yyyy-mm-dd date into dd-mm-yyyy for showing to the user."""
    try:
        return datetime.datetime.strptime(saved_date, "%Y-%m-%d").strftime("%d-%m-%Y")
    except ValueError:
        return saved_date


def display_month(saved_month: str) -> str:
    """Turn a saved yyyy-mm month into mm-yyyy for showing to the user."""
    try:
        return datetime.datetime.strptime(saved_month, "%Y-%m").strftime("%m-%Y")
    except ValueError:
        return saved_month
