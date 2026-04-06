from datetime import date

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .budget import build_month_calendar
from .payday import get_strategy


@csrf_exempt
def index(request):
    if request.method != "GET":
        return redirect("daily_expensable")
    strategy = get_strategy(request.GET.get("strategy"))
    context = build_month_calendar(date.today(), strategy=strategy)
    return render(request, "calculator/index.html", context)
