from .budget_data import budget_data


def get_total_income():
    return sum(i["amount"] for i in budget_data["incomes"])


def get_total_expenses():
    return sum(e["amount"] for e in budget_data["expenses"])


def get_balance():
    return get_total_income() - get_total_expenses()