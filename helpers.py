import datetime


def get_date_time() -> tuple[str, str]:
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")
    return date, time


def build_menu(options: list[str]) -> str:
    menu = ""
    for i in range(len(options)):
        menu += f"{i + 1}: {options[i]}  "
    return menu
    for i in range(len(options)):
        menu += f"{i + 1}: {options[i]}  "
    return menu


def select_from_list(prompt: str, items: list[str]) -> int:
    """Show a numbered menu and return the chosen position (starting at 0), or -1 if invalid."""
    print(build_menu(items))
    try:
        number: int = int(input(prompt).strip())
    except ValueError:
        return -1
    if 1 <= number <= len(items):
        return number - 1
    return -1


def convert_date(date_text: str) -> str:
    """Turn a dd-mm-yyyy date into yyyy-mm-dd for saving. Returns "" if it isn't a valid date."""
    try:
        entered = datetime.datetime.strptime(date_text, "%d-%m-%Y")
    except ValueError:
        return ""
    return entered.strftime("%Y-%m-%d")
