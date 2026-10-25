import category
import goals
import helpers
import storage

# import summary
import transaction

# Global variables
default_categories = ["Rent", "Food", "Salary"]
expenseType = ["expense", "income"]
options = [
    "Transaction menu",
    "Category menu",
    "Search transactions",
    "Goals menu",
    "Exit",
]

goal_options = [
    "Set goal",
    "Check goals",
    "Delete goal",
]

goal_types = ["spending limit", "saving"]

category_options = [
    "Add category",
    "Edit category",
    "Delete category",
    "List categories",
]

transaction_options = [
    "Add transaction",
    "Edit transaction",
    "Delete transaction",
]

edit_fields = ["amount", "type", "category", "date", "time", "description"]

search_fields = ["date", "category", "type", "description"]

date_time_options = ["Use current date and time", "Enter manually"]

# load files
categories, transactions, goal_list = storage.load_file(default_categories)


# create and format menus
main_menu = helpers.build_menu(options)
expense_type_menu = helpers.build_menu(expenseType)
category_menu = helpers.build_menu(category_options)
transaction_menu = helpers.build_menu(transaction_options)
goal_menu = helpers.build_menu(goal_options)


def show_main_menu() -> None:
    print(transaction.build_transaction_table(transactions))
    print(main_menu)


# Print block for the UI
show_main_menu()

while True:
    try:
        menu_input: int = int(input("Selected menu item: ").strip())
    except ValueError:
        menu_input = 0

    if menu_input == 1:
        while True:
            print(transaction_menu)
            choice: str = input(
                "Select menu option (leave blank for main menu): "
            ).strip()
            if choice == "":
                show_main_menu()
                break
            try:
                selected_menu_option: int = int(choice)
            except ValueError:
                selected_menu_option = 0

            if selected_menu_option == 1:
                try:
                    amount: float = float(input("Enter amount: ").strip())
                except ValueError:
                    amount = -1

                print(expense_type_menu)
                try:
                    type_number: int = int(input("Select expense type: ").strip())
                except ValueError:
                    type_number = 0

                print(helpers.build_menu(categories))
                try:
                    category_number: int = int(input("Select category: ").strip())
                except ValueError:
                    category_number = 0

                if amount <= 0:
                    print("Enter a valid amount")
                elif not 1 <= type_number <= len(expenseType):
                    print("Enter a valid expense type")
                elif not 1 <= category_number <= len(categories):
                    print("Enter a valid category number")
                else:
                    expense_type: str = expenseType[type_number - 1]
                    expense_category: str = categories[category_number - 1]
                    date_time_index: int = helpers.select_from_list(
                        "Select date and time option: ", date_time_options
                    )
                    if date_time_index == 1:
                        entered_date: str = input("Enter date (dd-mm-yyyy): ").strip()
                        expense_date: str = helpers.convert_date(entered_date)
                        if expense_date == "":
                            print("Enter a valid date (dd-mm-yyyy)")
                            continue
                        expense_time: str = input("Enter time (24 hour): ").strip()
                    else:
                        expense_date, expense_time = helpers.get_date_time()
                    expense_description: str = input("Enter description: ").strip()
                    new_id: int = transaction.add_transaction(
                        transactions,
                        amount,
                        expense_type,
                        expense_category,
                        expense_date,
                        expense_time,
                        expense_description,
                    )
                    storage.write_file(transactions=transactions)
                    print(f"Added transaction {new_id}")
            elif selected_menu_option == 2:
                print(transaction.build_transaction_table(transactions))
                try:
                    edit_id: int = int(input("Transaction ID to edit: ").strip())
                except ValueError:
                    edit_id = 0

                if edit_id not in transactions:
                    print("Transaction not found")
                else:
                    field_index: int = helpers.select_from_list(
                        "Select field to edit: ", edit_fields
                    )
                    if field_index == -1:
                        print("Enter a valid field")
                    else:
                        field: str = edit_fields[field_index]
                        new_value = None

                        if field == "amount":
                            try:
                                new_amount: float = float(input("New amount: ").strip())
                            except ValueError:
                                new_amount = -1
                            if new_amount > 0:
                                new_value = new_amount
                            else:
                                print("Enter a valid amount")
                        elif field == "type":
                            type_index: int = helpers.select_from_list(
                                "Select expense type: ", expenseType
                            )
                            if type_index == -1:
                                print("Enter a valid expense type")
                            else:
                                new_value = expenseType[type_index]
                        elif field == "category":
                            category_index: int = helpers.select_from_list(
                                "Select category: ", categories
                            )
                            if category_index == -1:
                                print("Enter a valid category number")
                            else:
                                new_value = categories[category_index]
                        elif field == "date":
                            converted_date: str = helpers.convert_date(
                                input("New date (dd-mm-yyyy): ").strip()
                            )
                            if converted_date == "":
                                print("Enter a valid date (dd-mm-yyyy)")
                            else:
                                new_value = converted_date
                        else:
                            new_value = input(f"New {field}: ").strip()

                        if new_value is not None:
                            transaction.edit_transaction(
                                transactions, edit_id, field, new_value
                            )
                            storage.write_file(transactions=transactions)
                            print(f"Updated {field} for transaction {edit_id}")
            elif selected_menu_option == 3:
                print(transaction.build_transaction_table(transactions))
                try:
                    delete_id: int = int(input("Transaction ID to delete: ").strip())
                except ValueError:
                    delete_id = 0

                if delete_id not in transactions:
                    print("Transaction not found")
                else:
                    confirm: str = (
                        input(f"Delete transaction {delete_id}? (y/n): ")
                        .strip()
                        .lower()
                    )
                    if confirm == "y":
                        transaction.delete_transaction(transactions, delete_id)
                        storage.write_file(transactions=transactions)
                        print(f"Deleted transaction {delete_id}")
                    else:
                        print("Delete cancelled")
            else:
                print("Enter a valid option")

    elif menu_input == 2:
        while True:
            print(category_menu)
            choice = input("Select menu option (leave blank for main menu): ").strip()
            if choice == "":
                show_main_menu()
                break
            try:
                selected_menu_option = int(choice)
            except ValueError:
                selected_menu_option = 0

            if selected_menu_option == 1:
                new_category: str = input("Name of the new category: ").strip()
                if new_category == "":
                    print("Category name cannot be blank")
                elif category.add_category(new_category, categories):
                    storage.write_file(categories=categories)
                    print(f"Added {new_category}")
                else:
                    print(f"{new_category} already exists")
            elif selected_menu_option == 2:
                print(helpers.build_menu(categories))
                try:
                    edit_number: int = int(
                        input("Number of category to edit: ").strip()
                    )
                except ValueError:
                    edit_number = 0
                if 1 <= edit_number <= len(categories):
                    old_name: str = categories[edit_number - 1]
                    new_name: str = input(f"New name for {old_name}: ").strip()
                    if new_name == "":
                        print("Category name cannot be blank")
                    elif category.edit_category(old_name, new_name, categories):
                        transaction.rename_category(transactions, old_name, new_name)
                        storage.write_file(
                            categories=categories, transactions=transactions
                        )
                        print(f"Renamed {old_name} to {new_name}")
                    else:
                        print(f"{new_name} already exists")
                else:
                    print("Enter a valid category number")
            elif selected_menu_option == 3:
                print(helpers.build_menu(categories))
                try:
                    delete_number: int = int(
                        input("Number of category to delete: ").strip()
                    )
                except ValueError:
                    delete_number = 0
                if 1 <= delete_number <= len(categories):
                    remove_name: str = categories[delete_number - 1]
                    category.remove_category(remove_name, categories)
                    storage.write_file(categories=categories)
                    print(f"Deleted {remove_name}")
                else:
                    print("Enter a valid category number")
            elif selected_menu_option == 4:
                print(helpers.build_menu(categories))
            else:
                print("Enter a valid option")

    elif menu_input == 3:
        while True:
            search_index: int = helpers.select_from_list(
                "Search by (leave blank for main menu): ", search_fields
            )
            if search_index == -1:
                show_main_menu()
                break
            search_field: str = search_fields[search_index]

            if search_field == "category":
                search_category_index: int = helpers.select_from_list(
                    "Select category: ", categories
                )
                if search_category_index == -1:
                    print("Enter a valid category number")
                    continue
                results = transaction.search_transactions(
                    transactions,
                    search_field,
                    categories[search_category_index],
                    exact=True,
                )
            elif search_field == "type":
                search_type_index: int = helpers.select_from_list(
                    "Select expense type: ", expenseType
                )
                if search_type_index == -1:
                    print("Enter a valid expense type")
                    continue
                results = transaction.search_transactions(
                    transactions,
                    search_field,
                    expenseType[search_type_index],
                    exact=True,
                )
            else:
                search_term: str = input(
                    f"Enter {search_field} to search for: "
                ).strip()
                results = transaction.search_transactions(
                    transactions, search_field, search_term
                )

            print(transaction.build_transaction_table(results))

    elif menu_input == 4:
        while True:
            print(goal_menu)
            choice = input("Select menu option (leave blank for main menu): ").strip()
            if choice == "":
                show_main_menu()
                break
            try:
                selected_menu_option = int(choice)
            except ValueError:
                selected_menu_option = 0

            if selected_menu_option == 1:
                goal_type_index: int = helpers.select_from_list(
                    "Select goal type: ", goal_types
                )
                if goal_type_index == -1:
                    print("Enter a valid goal type")
                    continue
                goal_type: str = goal_types[goal_type_index]

                goal_category: str = ""
                if goal_type == "spending limit":
                    goal_category_index: int = helpers.select_from_list(
                        "Select category: ", categories
                    )
                    if goal_category_index == -1:
                        print("Enter a valid category number")
                        continue
                    goal_category = categories[goal_category_index]

                try:
                    goal_amount: float = float(input("Goal amount: ").strip())
                except ValueError:
                    goal_amount = -1
                if goal_amount <= 0:
                    print("Enter a valid amount")
                    continue

                # date is yyyy-mm-dd, so the first 7 characters are yyyy-mm
                today, now_time = helpers.get_date_time()
                current_month: str = today[:7]
                goal_month: str = input(
                    f"Enter month (yyyy-mm, leave blank for {current_month}): "
                ).strip()
                if goal_month == "":
                    goal_month = current_month

                goals.set_goal(
                    goal_list, goal_type, goal_amount, goal_month, goal_category
                )
                storage.write_file(goals=goal_list)
                print("Goal added")
            elif selected_menu_option == 2:
                if len(goal_list) == 0:
                    print("No goals set")
                else:
                    for i in range(len(goal_list)):
                        print(
                            f"{i + 1}: {goals.check_goal(goal_list[i], transactions)}"
                        )
            elif selected_menu_option == 3:
                if len(goal_list) == 0:
                    print("No goals set")
                else:
                    goal_descriptions: list[str] = []
                    for goal in goal_list:
                        goal_descriptions.append(goals.check_goal(goal, transactions))
                    delete_goal_index: int = helpers.select_from_list(
                        "Number of goal to delete: ", goal_descriptions
                    )
                    if delete_goal_index == -1:
                        print("Enter a valid goal number")
                    else:
                        goal_list.pop(delete_goal_index)
                        storage.write_file(goals=goal_list)
                        print("Goal deleted")
            else:
                print("Enter a valid option")

    elif menu_input == 5:
        break
    else:
        print("Enter a valid option")
