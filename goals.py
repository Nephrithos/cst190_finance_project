"""Goal logic: storing monthly goals and working out progress.

Two kinds of goal (see storage.py for the stored format):
  spending limit   expenses in one category for a month must stay under the amount
  saving           income minus expenses for a month should reach the amount

Progress isn't stored; it's calculated from the transactions every time.
"""

import helpers


def set_goal(
    goal_list: list[dict],
    goal_type: str,
    amount: float,
    month: str,
    category: str = "",
) -> None:
    """Add a goal. month is "yyyy-mm". category is only used for spending limits."""
    goal_list.append(
        {
            "type": goal_type,
            "amount": amount,
            "month": month,
            "category": category,
        }
    )


def goal_exists(
    goal_list: list[dict], goal_type: str, month: str, category: str
) -> bool:
    """Return True if a goal of this type, month and category is already set."""
    for goal in goal_list:
        if (
            goal["type"] == goal_type
            and goal["month"] == month
            and goal["category"] == category
        ):
            return True
    return False


def rename_category(goal_list: list[dict], old_name: str, new_name: str) -> None:
    """Update every goal using old_name to use new_name instead."""
    for goal in goal_list:
        if goal["category"] == old_name:
            goal["category"] = new_name


def category_in_use(goal_list: list[dict], category: str) -> bool:
    """Return True if any goal uses this category."""
    for goal in goal_list:
        if goal["category"] == category:
            return True
    return False


def _month_total(
    transactions: dict[int, dict], month: str, expense_type: str, category: str = ""
) -> float:
    """Add up transactions of one type in a month, optionally for one category only."""
    total = 0.0
    for transaction_id in transactions:
        t = transactions[transaction_id]
        if t["date"].startswith(month) and t["type"] == expense_type:
            if category == "" or t["category"] == category:
                total += t["amount"]
    return total


def check_goal(goal: dict, transactions: dict[int, dict]) -> str:
    """Return a one-line description of how a goal is going."""
    target = goal["amount"]
    month = helpers.display_month(goal["month"])
    money = helpers.format_money

    if goal["type"] == "spending limit":
        spent = _month_total(transactions, goal["month"], "expense", goal["category"])
        remaining = target - spent
        label = f"{goal['category']} limit {month}"
        if remaining >= 0:
            return f"{label}: spent {money(spent)} of {money(target)} ({money(remaining)} left)"
        return f"{label}: spent {money(spent)} of {money(target)} (OVER by {money(-remaining)})"

    income = _month_total(transactions, goal["month"], "income")
    expenses = _month_total(transactions, goal["month"], "expense")
    saved = income - expenses
    label = f"Saving goal {month}"
    if saved >= target:
        return f"{label}: saved {money(saved)} of {money(target)} (REACHED)"
    return f"{label}: saved {money(saved)} of {money(target)} ({money(target - saved)} to go)"
