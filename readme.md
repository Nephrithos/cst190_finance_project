# Personal Finance Tracker

A command-line app for tracking income and expenses, built in Python for the CST 190 assignment.

Record transactions, organise them into categories, search them, set monthly spending and saving goals, and print reports, all from a menu in the terminal. Data is saved automatically to JSON files after every change.

## Features

- **Transactions:** add, edit and delete income and expenses, with the date and time filled in automatically or entered by hand
- **Transaction table:** every transaction shown on the main screen, sorted by date and time
- **Categories:** add, rename and delete categories. Renaming updates every transaction and goal that uses the category
- **Search:** find transactions by day, month or year, by category, by type, or by words in the description
- **Goals:** monthly spending limits per category, and monthly saving targets, with live progress
- **Reports:** all-time or single-month totals, spending per category with percentages, and a month-by-month breakdown
- **Validation:** every input is checked as it's typed, and the app asks again with an example until it's valid
- **Safe storage:** data folder and files are created on first run; damaged files are backed up rather than overwritten

## Requirements

- Python 3.10 or later (the code uses `X | None` type hints)
- No third-party packages; only the standard library (`json`, `os`, `datetime`)

## Getting started

```bash
git clone <your-repo-url>
cd <repo-folder>
python main.py
```

On first run, a `data/` folder is created next to the code with three default categories: Rent, Food and Salary.

Press Ctrl+C at any time to exit. Every change is saved as soon as it's made.

## Using the app

The main screen shows all transactions and the main menu:

```
-------------------------------------------------------------------------------------
ID    Date        Time   Type     Category               Amount  Description
-------------------------------------------------------------------------------------
1     01-10-2026  09:00  income   Salary              $3,000.00  October pay
2     01-10-2026  12:30  expense  Rent                $1,200.00  Rent
3     25-10-2026  13:15  expense  Food                   $24.50  Lunch
-------------------------------------------------------------------------------------
1: Transaction menu  2: Category menu  3: Search transactions  4: Goals menu  5: Reports  6: Exit
```

Choose an option by typing its number. In any submenu, leave the choice blank and press Enter to go back to the main menu.

### Input formats

| What | Format | Example |
| --- | --- | --- |
| Amount | Positive number, at most 2 decimal places (`$` and commas allowed) | `24.50`, `$1,200` |
| Date | `dd-mm-yyyy` | `25-10-2026` |
| Time | 24 hour `hh:mm` | `13:15` |
| Month (goals, reports) | `mm-yyyy`, or blank for this month | `10-2026` |
| Date search | A day, a month or a year | `25-10-2026`, `10-2026`, `2026` |

### Goals

- **Spending limit:** total expenses in one category for a month should stay under the amount. Shows how much is left, or how far over you are.
- **Saving:** income minus expenses for a month should reach the amount.

Progress is worked out from your transactions every time you check, so it is always up to date.

### Categories

Category names are case-insensitive ("food" and "Food" are the same) and up to 15 characters. A category can't be deleted while transactions or goals use it, and the last category can't be deleted.

## Project structure

```
main.py                 Entry point: loads data and runs the main menu
config.py               Menu options, allowed values and length limits

menu_transactions.py    Transaction menu: add, edit, delete
menu_categories.py      Category menu: add, rename, delete, list
menu_search.py          Search menu
menu_goals.py           Goals menu: set, check, delete
menu_reports.py         Reports menu

transaction.py          Transaction logic: add, edit, delete, search, table
category.py             Category list logic
goals.py                Goal logic and progress
summary.py              Report calculations and formatting

helpers.py              Validated input, menus, date and money formatting
storage.py              Loading, checking and saving the JSON files
```

The code is in three layers:

1. **Menus** ask the user for input, then call the logic.
2. **Logic** modules change and calculate data. They never call `input()` or save, so they can be tested on their own.
3. **Support** modules (`helpers.py`, `storage.py`, `config.py`) are shared by everything.

Data is loaded once in `main.py` and passed into each menu, which changes it in place and saves straight away.

## Data storage

Data is saved in `data/` as JSON:

| File | Contents |
| --- | --- |
| `categories.json` | List of category names |
| `transaction.json` | Transactions, keyed by ID |
| `goals.json` | List of goals |
| `counters.json` | The next transaction ID to use |

Some design decisions worth knowing:

- **Money is stored in whole cents** (`2550` means $25.50), so totals are exact. Floating-point maths would make 0.10 + 0.20 come out as 0.30000000000000004.
- **Dates are stored year-first** (`2026-10-25`), even though you type them day-first. Year-first dates sort correctly as text and make searching a whole month easy (everything starting with `2026-10`).
- **Transaction IDs are never reused.** A saved counter only ever goes up, so deleting a transaction can't cause its ID to be given to a new one.
- **Categories are stored by name** in transactions and goals, not by list position, so they stay correct if the category list changes.

The full format of each file is described at the top of `storage.py`.

## Known limitations

- No automated tests yet.
- Deleting a category that's in use is blocked rather than offering to move its transactions to another category.
- Files are written directly rather than through a temporary file, so a crash mid-save could damage one.
- Single user, single currency, terminal only.

## Author

<Your name>, CST 190
