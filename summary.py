REPORT_WIDTH = 52


def _money(amount: float) -> str:
    """Format an amount as $1,234.50, with the minus sign in front of the $."""
    if amount < 0:
        return f"-${-amount:,.2f}"
    return f"${amount:,.2f}"


def calculate_totals(transactions: dict[int, dict]) -> tuple[float, float, float]:
    """Return (total income, total expenses, net) for the given transactions."""
    income = 0.0
    expenses = 0.0
    for transaction_id in transactions:
        t = transactions[transaction_id]
        if t["type"] == "income":
            income += t["amount"]
        else:
            expenses += t["amount"]
    return income, expenses, income - expenses


def spend_per_cat(transactions: dict[int, dict]) -> dict[str, float]:
    """Return total spending for each category (expenses only)."""
    totals: dict[str, float] = {}
    for transaction_id in transactions:
        t = transactions[transaction_id]
        if t["type"] == "expense":
            if t["category"] not in totals:
                totals[t["category"]] = 0.0
            totals[t["category"]] += t["amount"]
    return totals


def monthly_breakdown(transactions: dict[int, dict]) -> dict[str, dict[str, float]]:
    """Return income and expense totals for each month, keyed by "yyyy-mm"."""
    months: dict[str, dict[str, float]] = {}
    for transaction_id in transactions:
        t = transactions[transaction_id]
        month = t["date"][
            :7
        ]  # dates are yyyy-mm-dd, so the first 7 characters are yyyy-mm
        if month not in months:
            months[month] = {"income": 0.0, "expense": 0.0}
        months[month][t["type"]] += t["amount"]
    return months


def build_report(transactions: dict[int, dict], title: str) -> str:
    """Return a full report (totals, spending per category, monthly breakdown) ready to print."""
    line = "-" * REPORT_WIDTH
    report = f"{line}\n{title:^{REPORT_WIDTH}}\n{line}\n"

    if len(transactions) == 0:
        report += f"{'No transactions found':^{REPORT_WIDTH}}\n{line}"
        return report

    # Totals
    income, expenses, net = calculate_totals(transactions)
    report += f"{'Total income':<20}{_money(income):>32}\n"
    report += f"{'Total expenses':<20}{_money(expenses):>32}\n"
    report += f"{'Net':<20}{_money(net):>32}\n"
    report += line + "\n"

    # Spending per category
    report += f"{'Category':<20}  {'Spent':>14}  {'% of spending':>14}\n"
    category_totals = spend_per_cat(transactions)
    if len(category_totals) == 0:
        report += f"{'No spending':^{REPORT_WIDTH}}\n"
    else:
        for category_name in category_totals:
            spent = category_totals[category_name]
            percent = spent / expenses * 100
            report += (
                f"{category_name:<20.20}  {_money(spent):>14}  {percent:>13.1f}%\n"
            )
    report += line + "\n"

    # Monthly breakdown (yyyy-mm sorts correctly as text, oldest first)
    report += f"{'Month':<10}  {'Income':>12}  {'Expenses':>12}  {'Net':>12}\n"
    months = monthly_breakdown(transactions)
    for month in sorted(months):
        month_income = months[month]["income"]
        month_expenses = months[month]["expense"]
        report += (
            f"{month:<10}  {_money(month_income):>12}  "
            f"{_money(month_expenses):>12}  {_money(month_income - month_expenses):>12}\n"
        )
    report += line
    return report
