from django.shortcuts import render

FEATURES = [
    {
        "name": "Daily Expensable",
        "description": "Calculate how much you can spend per day until payday. "
                       "Visualise your month, exclude pre-budgeted days, and pick your payday strategy.",
        "url_name": "daily_expensable",
    },
    {
        "name": "Monthly Fixed Costs",
        "description": "Enter your income and fixed expenses — tax, social security, rent, "
                       "subscriptions — and see what's left each month.",
        "url_name": "fixed_costs",
    },
]


def home(request):
    return render(request, "core/home.html", {"features": FEATURES})
