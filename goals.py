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

    if goal["type"] == "spending limit":
        spent = _month_total(transactions, goal["month"], "expense", goal["category"])
        remaining = target - spent
        label = f"{goal['category']} limit {goal['month']}"
        if remaining >= 0:
            return (
                f"{label}: spent ${spent:.2f} of ${target:.2f} (${remaining:.2f} left)"
            )
        return (
            f"{label}: spent ${spent:.2f} of ${target:.2f} (OVER by ${-remaining:.2f})"
        )

    income = _month_total(transactions, goal["month"], "income")
    expenses = _month_total(transactions, goal["month"], "expense")
    saved = income - expenses
    label = f"Saving goal {goal['month']}"
    if saved >= target:
        return f"{label}: saved ${saved:.2f} of ${target:.2f} (REACHED)"
    return f"{label}: saved ${saved:.2f} of ${target:.2f} (${target - saved:.2f} to go)"
