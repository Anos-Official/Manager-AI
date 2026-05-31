budget_data = {
    "incomes": [],
    "expenses": []
}

CATEGORIES = [
    "Housing",
    "Food",
    "Transport",
    "Subscriptions",
    "Entertainment",
    "Other"
]


def add_income(name, amount):
    budget_data["incomes"].append({
        "name": name,
        "amount": amount
    })


def remove_income(index):
    budget_data["incomes"].pop(index)


def add_expense(name, category, amount):
    budget_data["expenses"].append({
        "name": name,
        "category": category,
        "amount": amount
    })


def remove_expense(index):
    budget_data["expenses"].pop(index)