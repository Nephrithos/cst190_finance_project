"""Goals menu: set, check and delete monthly goals.

Goals don't store progress. check_goal works it out from the transactions
every time, so progress is always up to date after adding or editing transactions.
"""

import config
import goals
import helpers
import storage


def set_goal_entry(goal_list: list[dict], categories: list[str]) -> None:
    """Ask for the goal's type, category (spending limits only), amount and month."""
    goal_type = helpers.choose_item("Select goal type: ", config.GOAL_TYPES)

    # Saving goals cover all income and spending, so they have no category
    goal_category = ""
    if goal_type == "spending limit":
        goal_category = helpers.choose_item("Select category: ", categories)

    goal_amount = helpers.get_amount("Goal amount: ")
    goal_month = helpers.get_month(
        f"Enter month (mm-yyyy, leave blank for {helpers.current_month_display()}): "
    )

    # Two goals for the same thing in the same month would just contradict each other
    if goals.goal_exists(goal_list, goal_type, goal_month, goal_category):
        print("That goal is already set for this month, delete it first to change it")
        return

    goals.set_goal(goal_list, goal_type, goal_amount, goal_month, goal_category)
    if storage.write_file(goals=goal_list):
        print("Goal added")
    else:
        print(config.SAVE_FAILED)


def check_goals_entry(goal_list: list[dict], transactions: dict[int, dict]) -> None:
    """Print every goal with its current progress."""
    if len(goal_list) == 0:
        print("No goals set")
        return
    for i in range(len(goal_list)):
        print(f"{i + 1}: {goals.check_goal(goal_list[i], transactions)}")


def delete_goal_entry(goal_list: list[dict], transactions: dict[int, dict]) -> None:
    """Show the goals as a numbered list, then delete the one picked."""
    if len(goal_list) == 0:
        print("No goals set")
        return

    # Use the progress lines as the menu, so the user can see which goal is which
    goal_descriptions: list[str] = []
    for goal in goal_list:
        goal_descriptions.append(goals.check_goal(goal, transactions))

    delete_index = helpers.select_from_list(
        "Number of goal to delete (leave blank to cancel): ",
        goal_descriptions,
        allow_blank=True,
    )
    if delete_index == -1:
        return

    if helpers.confirm("Delete this goal? (y/n): "):
        goal_list.pop(delete_index)
        if storage.write_file(goals=goal_list):
            print("Goal deleted")
        else:
            print(config.SAVE_FAILED)
    else:
        print("Delete cancelled")


def run(
    goal_list: list[dict], transactions: dict[int, dict], categories: list[str]
) -> None:
    """Show the goals menu until the user leaves it blank."""
    while True:
        choice = helpers.select_from_list(
            config.SUBMENU_PROMPT, config.GOAL_OPTIONS, allow_blank=True
        )
        if choice == -1:
            return
        if choice == 0:
            set_goal_entry(goal_list, categories)
        elif choice == 1:
            check_goals_entry(goal_list, transactions)
        else:
            delete_goal_entry(goal_list, transactions)
