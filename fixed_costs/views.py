from django.shortcuts import render

DEFAULT_DEDUCTIONS = [
    {"name": "Tax", "amount": ""},
    {"name": "Social Security", "amount": ""},
    {"name": "Rent", "amount": ""},
    {"name": "Utilities", "amount": ""},
    {"name": "Insurance", "amount": ""},
    {"name": "Subscriptions", "amount": ""},
]


def index(request):
    return render(request, "fixed_costs/index.html", {
        "default_deductions": DEFAULT_DEDUCTIONS,
    })
