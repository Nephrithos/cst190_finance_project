"""Reports menu: print an all-time or single-month report.

The report itself is built by summary.py. A single-month report is just the
same report run on the transactions from that month.
"""

import config
import helpers
import summary
import transaction


def run(transactions: dict[int, dict]) -> None:
    """Ask which report to show, print it, and repeat until left blank."""
    while True:
        choice = helpers.select_from_list(
            "Select report (leave blank for main menu): ",
            config.REPORT_OPTIONS,
            allow_blank=True,
        )
        if choice == -1:
            return

        if choice == 0:
            print(summary.build_report(transactions, "All time report"))
        else:
            # get_month returns yyyy-mm, and saved dates start with yyyy-mm,
            # so a date search with it finds every transaction in that month
            report_month = helpers.get_month(
                f"Enter month (mm-yyyy, leave blank for {helpers.current_month_display()}): "
            )
            month_transactions = transaction.search_transactions(
                transactions, "date", report_month
            )
            title = f"Report for {helpers.display_month(report_month)}"
            print(summary.build_report(month_transactions, title))
